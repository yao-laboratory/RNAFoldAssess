import os, datetime

from RNAFoldAssess.models.predictors import *
from RNAFoldAssess.models.scorers import *
from RNAFoldAssess.models import DataPoint
from RNAFoldAssess.utils.secondary_structure_tools import SecondaryStructureTools


model_name = "RNAFold"
model = RNAFold()
model_path = os.path.abspath("/home/yesselmanlab/ewhiting/ViennaRNA/bin/RNAfold")

ribo_data_csv = "/common/yesselmanlab/ewhiting/data/ribonanza/rmdb_data.v1.3.0.csv"
f = open(ribo_data_csv)
data = f.readlines()
f.close()

# Get rid of headers
data.pop(0)
data = [d.split(",") for d in data]

r1_index = 7
# Experiment types:
# We need to redo 1M7
experiment_map = {
    "1M7": "SHAPE",
}

report_path = "/common/yesselmanlab/ewhiting/reports/ribonanza/with_energies"

report_files = {}
problem_files = {}
for k in experiment_map:
    f = open(f"{report_path}/{model_name}_{k}_predictions.txt", "w")
    report_files[k] = f
    f2 = open(f"{report_path}/{model_name}_{k}_problems.txt", "w")
    problem_files[k] = f


print(f"Length before filtering: {len(data)}")
data = [d for d in data if d[2] == "1M7"]
print(f"Length after filtering: {len(data)}")

len_data = len(data)

counter = 0
for d in data:
    if counter % 200 == 0:
        print(f"Working {counter} of {len_data}")
    name = d[0]
    seq = d[1]
    experiment_type = d[2]
    chemical_mapping_method = experiment_map[experiment_type]
    report_file = report_files[experiment_type]
    problem_file = problem_files[experiment_type]
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
    file_safe_name = "".join(c for c in name if c.isalnum())
    fasta_string = f">{file_safe_name}\n{sequence}"
    fasta_file = open(f"{file_safe_name}.fasta", "w")
    fasta_file.write(fasta_string)
    fasta_file.close()
    fasta_path = os.path.abspath(f"{file_safe_name}.fasta")
    try:
        model.execute(model_path, fasta_path)
        pred = model.get_ss_prediction()
        testable_prediction = pred[:len(sequence)]
        prediction = testable_prediction
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
        fe = model.get_prediction_fe()
        line_to_write = f"{model_name}, {name}, {testable_seq}, {testable_prediction}, {accuracy}, {p}, {fe}\n"
        report_file.write(line_to_write)
        counter += 1

    except (DSCITypeError, DSCIValueError) as dsci_error:
        problem_to_write = f"{name}, {dsci_error}, {prediction}\n"
        problem_file.write(problem_to_write)
        continue

    except Exception as e:
        problem_to_write = f"{name}, {e}\n"
        problem_file.write(problem_to_write)


for k in experiment_map:
    report_files[k].close()
    problem_files[k].close()
