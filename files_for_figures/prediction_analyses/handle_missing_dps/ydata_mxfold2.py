import os


from RNAFoldAssess.models import DataPoint
from RNAFoldAssess.models.scorers import *
from RNAFoldAssess.models.predictors import MXFold2


dp_file_path = "/common/yesselmanlab/ewhiting/ss_deeplearning_data/data"

model_name = "MXFold2"
model = MXFold2()
approved_chorots = [
    "C014U",
    "C014V"
]
data_point_files = os.listdir(dp_file_path)


with open("../MXFold2_missing_dps.txt") as r:
    missing_dps = [line.strip() for line in r.readlines()]


u_missing_ydata = [md for md in missing_dps if md[:5] == "C014U"]
v_missing_ydata = [md for md in missing_dps if md[:5] == "C014V"]

analysis_report_path = f"/mnt/nrdstor/yesselmanlab/ewhiting/reports/ydata/{model_name}_remaining.txt"

data_points = []
for dpf in data_point_files:
    cohort = dpf.split(".")[0]
    if cohort not in approved_chorots:
        continue
    print(f"Loading data points from {cohort} cohort")
    dps = DataPoint.factory(f"{dp_file_path}/{dpf}", cohort)
    for dp in dps:
        if dp.name in missing_dps:
            data_points.append(dp)

dp_size = len(data_points)
print(f"Total of {dp_size} data points")
print("Data points loaded!")

counter = 0
rows_to_write = []
f = open(analysis_report_path, "a")
for dp in data_points:
    if counter % 250 == 0:
        print(f"Completed {counter} of {dp_size}")

    input_file_path = f"/work/yesselmanlab/ewhiting/reverse_experiment/fasta_files/{dp.cohort}/{dp.name}.fasta"
    try:
        model.execute(input_file_path)
        prediction = model.get_ss_prediction()

        score = DSCI.score(
            dp.sequence,
            prediction,
            dp.reactivities,
            DMS=True
        )

        accuracy = score["accuracy"]
        p = score["p"]

        line_to_write = f"{model_name}, {dp.name}, {dp.sequence}, {prediction}, {accuracy}, {p}\n"
        f.write(line_to_write)

        counter += 1

    except (DSCITypeError, DSCIValueError) as dsci_error:
        print(f"Encountered DSCI error on {dp.name}: {str(dsci_error)}")
        continue
