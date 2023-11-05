import os, datetime


from RNAFoldAssess.models import DataPoint
from RNAFoldAssess.models.scorers import DSCI, DSCITypeError, DSCIValueError
from RNAFoldAssess.models.predictors import *

eterna = Eterna()
eterna_path = os.path.abspath("/home/yesselmanlab/ewhiting/EternaFold")

dp_path = "/common/yesselmanlab/ewhiting/ss_deeplearning_data/data"
data_point_files = os.listdir(dp_path)

print(f"Loading data points from {len(data_point_files)} files ...")

data_points = []
for dpf in data_point_files:
    cohort = dpf.split(".")[0]
    print(f"Loading data points from {cohort} cohort")
    dps = DataPoint.factory(f"{dp_path}/{dpf}", cohort)
    for dp in dps:
        data_points.append(dp)

dp_size = len(data_points)
print(f"Total of {dp_size} data points")
print("Data points loaded!")

# For testing
# data_points = data_points[17360:17380] # There's an error-prone data point in here

print("Writing headers ...")
headers = "algo_name, datapoint_name, accuracy, p_value, ground_truth_data_type"
f = open("/common/yesselmanlab/ewhiting/reports/eterna_dms_pipeline_report.txt", "w")
f.write(f"{headers}\n")

# For info on dataset later
lengths = []
accuracies = []
p_values = []

print("About to run evaluation ...")
counter = 0
lowest_acc = [None, 1.0]
highest_p = [None, 1.0]
skipped_count = 0
one_point_oh_accuracies = 0

for dp in data_points:
    if counter % 250 == 0:
        print(f"Completed {counter} of {dp_size}")
    lengths.append(len(dp.sequence))
    input_file_path = dp.to_seq_file()
    eterna.execute(eterna_path, input_file_path)
    prediction = eterna.get_ss_prediction()
    try:
        score = DSCI.score(
            dp.sequence,
            prediction,
            dp.reactivities,
            DMS=True
        )
        accuracy = round(score["accuracy"], 4)
        p = round(score["p"], 4)

        accuracies.append(accuracy)
        p_values.append(p)

        if accuracy < lowest_acc[1]:
            lowest_acc = [dp.name, accuracy]

        if accuracy == 1.0:
            one_point_oh_accuracies += 1

        if p > highest_p[1]:
            highest_p = [dp.name, p]

        f.write(f"EternaFold, {dp.name}, {accuracy}, {p}, DMS\n")
        counter += 1
    except (DSCITypeError, DSCIValueError) as dsci_error:
        skipped_count += 1
        print(f"Encountered DSCI error on {dp.name}: {str(dsci_error)}")
        continue

f.close()

# about dataset
f2 = open("/common/yesselmanlab/ewhiting/reports/about_pipeline_eterna_dms.txt", "w")
avg_seq_len = sum(lengths) / len(lengths)
max_len = max(lengths)
min_len = min(lengths)
mode_len = max(set(lengths), key=lengths.count)

avg_acc = sum(accuracies) / len(accuracies)
mode_acc = max(set(accuracies), key=accuracies.count)
avg_p   = sum(p_values) / len(p_values)

about_data = ""
about_data += f"About DMS Data from Yesselman Lab\n"
about_data += f"Average sequence length: {avg_seq_len}\n"
about_data += f"Longest sequence: {max_len}\n"
about_data += f"Shortest sequence: {min_len}\n"
about_data += f"Most common sequence length: {mode_len}\n"

about_data += f"\nSkipped {skipped_count} molecules due to exceptions\n"

about_data += f"\EternaFold Performance:\n"
about_data += f"Average DSCI accuracy score: {round(avg_acc, 4)}\n"
about_data += f"Average DSCI p-vale score: {avg_p}\n"
about_data += f"Mode accuracy: {mode_acc}\n"
about_data += f"Number of DSCI 1.0 scores: {one_point_oh_accuracies}\n"
about_data += f"Lowest DSCI accruracy score: {lowest_acc[1]} on {lowest_acc[0]}\n"
about_data += f"Highest DSCI p-value score: {highest_p[1]} on {highest_p[0]}\n"

about_data += f"\n"
about_data += f"Report generated on: {datetime.datetime.now()}\n\n"

f2.write(about_data)
f2.close()

