import os


from RNAFoldAssess.models.scorers import DSCI
from RNAFoldAssess.models import DataPoint


model_name = "SPOT-RNA"
dbn_dir = "/work/yesselmanlab/ewhiting/spot_outputs/ribonanza/dbn_files"
ribo_data_csv = "/mnt/nrdstor/yesselmanlab/ewhiting/rna_data/ribonanza/rmdb_data.v1.3.0.csv"
f = open(ribo_data_csv)
data = f.readlines()
f.close()
# Get rid of headers
data.pop(0)
data = [d.split(",") for d in data]
r1_index = 7
# Experiment types:
# {'BzCN_cotx', 'deg_Mg_50C', 'BzCN', 'DMS_M2_seq', 'deg_pH10', 'deg_Mg_pH10', 'DMS_cotx', 'deg_50C', 'NMIA', 'DMS', 'CMCT', '1M7'
experiment_map = {
    "BzCN_cotx": "DMS4",
    "DMS_M2_seq": "DMS4",
    "DMS_cotx": "DMS4",
    "DMS": "DMS4",
    "1M7": "SHAPE",
    "NMIA": "SHAPE",
    "BzCN": "SHAPE",
    "deg_Mg_50C": "SHAPE",
    "deg_50C": "SHAPE",
    "deg_pH10": "SHAPE",
    "deg_Mg_pH10": "SHAPE",
    "CMCT": "CMCT"
}
report_path = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/ribonanza/with_energies"

# Create report file map
report_files = {}
for k in experiment_map:
    f = open(f"{report_path}/{model_name}_{k}_predictions.txt", "w")
    report_files[k] = f

# Run Evaluations
print("Starting evaluations")
counter = 0
for d in data:
    name = d[0]
    seq = d[1]
    experiment_type = d[2]
    chemical_mapping_method = experiment_map[experiment_type]
    report_file = report_files[experiment_type]
    reactivities = d[r1_index:len(seq) + r1_index]
    testable_seq = ""
    testable_reactivities = []
    for i, reactivity in enumerate(reactivities):
        if reactivity != "":
            testable_seq += seq[i]
            testable_reactivities.append(float(reactivity))

    sequence = testable_seq
    reactivities = testable_reactivities
    if len(sequence) < 2:
        # Can't predict secondary structure on one nucleotide
        continue

    dp = DataPoint({
        "name": name,
        "sequence": sequence,
        "data": reactivities,
        "reads": 0
    })
    if counter % 200 == 0:
        print(f"Completed {counter} of {len(data)}")

    try:
        dbn_file = f"{dbn_dir}/{name}.ct.dbn"
        with open(dbn_file) as df:
            dbn_data = df.readlines()
        prediction = dbn_data[2].strip()

        testable_prediction = prediction[:len(sequence)]

        if chemical_mapping_method in ["DMS4", "SHAPE"]:
            score = DSCI.score(
                sequence,
                testable_prediction,
                reactivities,
                SHAPE=True
            )
        else:
            score = DSCI.score(
                sequence,
                testable_prediction,
                reactivities,
                CMCT=True
            )

        accuracy = round(score["accuracy"], 4)
        p = round(score["p"], 4)

        line_to_write = f"{model_name}, {dp.name}, {testable_seq}, {testable_prediction}, {accuracy}, {p}\n"
        report_file.write(line_to_write)
        counter += 1

    except Exception as e:
        print(f"Problem with {name}: {e}")
        continue

print("Done")
