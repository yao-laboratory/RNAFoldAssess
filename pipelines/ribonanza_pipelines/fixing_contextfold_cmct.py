import os, datetime, time

from RNAFoldAssess.utils import *
from RNAFoldAssess.models.predictors import *
from RNAFoldAssess.models.scorers import *
from RNAFoldAssess.utils.secondary_structure_tools import SecondaryStructureTools


model = ContextFold()
model_name = "ContextFold"
model_path = os.path.abspath("/home/yesselmanlab/ewhiting/ContextFold_1_00")

ribo_data_csv = "/common/yesselmanlab/ewhiting/data/ribonanza/rmdb_data.v1.3.0.csv"
f = open(ribo_data_csv)
data = f.readlines()
f.close()
data.pop(0)
# Get rid of headers
target_experiment_type = "CMCT"
data = [d.split(",") for d in data]
data = [d for d in data if d[2] == target_experiment_type]
# Get just CMCT data
r1_index = 7

report_path = "/common/yesselmanlab/ewhiting/reports/ribonanza"

# report_file = open(f"{report_path}/{model_name}_{target_experiment_type}_predictions.txt", "w")
# problem_file = open(f"{report_path}/{model_name}_{target_experiment_type}_problems.txt", "w")

# For testing
energy_data = data[100:200]
data = data[:100]

print("Starting evaluations")
counter = 0
length_skip_threshold = 10 # It's 10 for contextfold

reg_start = time.time()
for d in data:
    name = d[0]
    seq = d[1]
    experiment_type = d[2]
    if experiment_type != target_experiment_type:
        continue
    reactivities = d[r1_index:len(seq) + r1_index]
    testable_seq = ""
    testable_reactivities = []
    for i, reactivity in enumerate(reactivities):
        if reactivity != "":
            testable_seq += seq[i]
            testable_reactivities.append(float(reactivity))
    sequence = testable_seq
    if len(sequence) < length_skip_threshold:
        print(f"Skipping {name}, only {len(sequence)} nucleotides long")
        continue
    try:
        model.execute(model_path, sequence)
        prediction = model.get_ss_prediction()
        testable_prediction = prediction[:len(testable_seq)]
        score = DSCI.score(
            testable_seq,
            testable_prediction,
            testable_reactivities,
            CMCT=True
        )
        accuracy = round(score["accuracy"], 4)
        p = round(score["p"], 4)
        line_to_write = f"{model_name}, {name}, {testable_seq}, {testable_prediction}, {accuracy}, {p}\n"
        print(line_to_write)
        counter += 1
    except (DSCITypeError, DSCIValueError) as dsci_error:
        problem_to_write = f"{name}, {dsci_error}, {prediction}\n"
        print(problem_to_write)
        # problem_file.write(problem_to_write)
        continue

    except Exception as e:
        problem_to_write = f"{name}, {e}\n"
        print(problem_to_write)
        # problem_file.write(problem_to_write)

reg_end = time.time()
reg_elapsed = round(reg_end - reg_start, 2)

print("\n\n")
## Now check the time it takes to do the same thing but with energies
eng_start = time.time()
for d in energy_data:
    name = d[0]
    seq = d[1]
    experiment_type = d[2]
    if experiment_type != target_experiment_type:
        continue
    reactivities = d[r1_index:len(seq) + r1_index]
    testable_seq = ""
    testable_reactivities = []
    for i, reactivity in enumerate(reactivities):
        if reactivity != "":
            testable_seq += seq[i]
            testable_reactivities.append(float(reactivity))
    sequence = testable_seq
    if len(sequence) < length_skip_threshold:
        print(f"Skipping {name}, only {len(sequence)} nucleotides long")
        continue
    try:
        model.execute(model_path, sequence)
        prediction = model.get_ss_prediction()
        testable_prediction = prediction[:len(testable_seq)]
        score = DSCI.score(
            testable_seq,
            testable_prediction,
            testable_reactivities,
            CMCT=True
        )
        accuracy = round(score["accuracy"], 4)
        p = round(score["p"], 4)
        fe = SecondaryStructureTools.get_free_energy(testable_seq, testable_prediction)
        line_to_write = f"{model_name}, {name}, {testable_seq}, {testable_prediction}, {accuracy}, {p}, {fe}\n"
        print(line_to_write)
        counter += 1
    except (DSCITypeError, DSCIValueError) as dsci_error:
        problem_to_write = f"{name}, {dsci_error}, {prediction}\n"
        print(problem_to_write)
        # problem_file.write(problem_to_write)
        continue

    except Exception as e:
        problem_to_write = f"{name}, {e}\n"
        print(problem_to_write)
        # problem_file.write(problem_to_write)

eng_end = time.time()
eng_elapsed = round(eng_end - eng_start, 2)

print(f"Elapsed time for regular predictions: {reg_elapsed}")
print(f"Elapsed time for energy predictions: {eng_elapsed}")

# 947c056d35e9, TypeError failure reading sequence CGCUUCAUAUAAUCCUAAUGAUAUGGUUUGGGAGUUUCUACCAAGAGCCUUAAACUCUUGAUUAUGAAGUCUGUCGCUUUAUCCGAAAUUUUAUAAAGAGAAGACUCAUGAAU: ufunc 'isnan' not supported for the inp
# ut types, and the inputs could not be safely coerced to any supported types according to the casting rule ''safe'', (((((((((...((((((.........))))))........((((((.......))))))..))))))))......(((((......
# ......)))))..........)....
# 947c056d35e9, TypeError failure reading sequence CGCUUCAUAUAAUCCUAAUGAUAUGGUUUGGGAGUUUCUACCAAGAGCCUUAAACUCUUGAUUAUGAAGUCUGUCGCUUUAUCCGAAAUUUUAUAAAGAGAAGACUCAUGAAU: ufunc 'isnan' not supported for the inp
# ut types, and the inputs could not be safely coerced to any supported types according to the casting rule ''safe'', (((((((((...((((((.........))))))........((((((.......))))))..))))))))......(((((......
# ......)))))..........)....
# 32db00c23029, TypeError failure reading sequence CGCUUCAUAUAAUCCUAAUGAUAUGGUUUGGGAGUUUCUACCAAGAGCCUUAAACUCUUGAUUAUGAAGUCUGUCGCUUUAUCCGAAAUUUUAUAAAGAGAAGACUCAUGAAUUACUUUGACCUGCCG: ufunc 'isnan' not suppor
# ted for the input types, and the inputs could not be safely coerced to any supported types according to the casting rule ''safe'', (((((((((...((((((.........))))))........((((((.......))))))..))))))))..
# ....(((((............))))).........................)....
# 32db00c23029, TypeError failure reading sequence CGCUUCAUAUAAUCCUAAUGAUAUGGUUUGGGAGUUUCUACCAAGAGCCUUAAACUCUUGAUUAUGAAGUCUGUCGCUUUAUCCGAAAUUUUAUAAAGAGAAGACUCAUGAAUUACUUUGACCUGCCG: ufunc 'isnan' not suppor
# ted for the input types, and the inputs could not be safely coerced to any supported types according to the casting rule ''safe'', (((((((((...((((((.........))))))........((((((.......))))))..))))))))..
# ....(((((............))))).........................)....
# 5577f7d027c2, TypeError failure reading sequence CGCUUCAUAUAAUCCUAAUGAUAUGGUUUGGGAGUUUCUACCAAGAGCCUUAAACUCUUGAUUAUGAAGUC: ufunc 'isnan' not supported for the input types, and the inputs could not be safe
# ly coerced to any supported types according to the casting rule ''safe'', .((((((((...((((((.........))))))........((((((.......))))))..)))))))).
# 5577f7d027c2, TypeError failure reading sequence CGCUUCAUAUAAUCCUAAUGAUAUGGUUUGGGAGUUUCUACCAAGAGCCUUAAACUCUUGAUUAUGAAGUC: ufunc 'isnan' not supported for the input types, and the inputs could not be safe
# ly coerced to any supported types according to the casting rule ''safe'', .((((((((...((((((.........))))))........((((((.......))))))..)))))))).
# 3f9539b15737, Reactivities length (155) and secondary structure length (135) don't match.
