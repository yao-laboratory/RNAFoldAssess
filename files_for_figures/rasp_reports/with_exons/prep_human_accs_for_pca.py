import os


matched_set_path = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions/rasp_matched_set_human.txt"

with open(matched_set_path) as fh:
    lines = [line.strip().split(", ") for line in fh.readlines()]

models = [
    "ContextFold",
    "ContraFold",
    "EternaFold",
    "IPKnot",
    "MXFold",
    "MXFold2",
    "NeuralFold",
    "NUPACK",
    "pKnots",
    "RNAFold",
    "RNAStructure",
    "Simfold",
    "SPOT-RNA"
]

uniq_dps = set()

model_acc_map = {}
for m in models:
    model_acc_map[m] = {}

print("Building model<->accuracy map")
for line in lines:
    model = line[0]
    dp = line[1]
    acc = line[4]
    uniq_dps.add(dp)

    model_acc_map[model][dp] = acc

fstring_builder = {}
for m in models:
    fstring_builder[m] = []

print("Building filestrings")
for dp in uniq_dps:
    for m in models:
        acc = model_acc_map[m][dp]
        fstring_builder[m].append(acc)


print("Writing")
for m in models:
    fstring = ",".join(fstring_builder[m])
    with open(f"{m}_accs_for_human_pca.txt", "w") as fh:
        fh.write(fstring)

print("Done")
