import os

base_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions"
matched_file = f"{base_dir}/rasp_microbe_matched_set.txt"

with open(matched_file) as fh:
    lines = [d.split(", ") for d in fh.readlines()]


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

model_index = 0
dp_index = 1
acc_index = 4

dps = set([line[dp_index] for line in lines])
dps = list(dps)

dp_model_map = {}
for dp in dps:
    dp_model_map[dp] = {}

for line in lines:
    dp = line[dp_index]
    model = line[model_index]
    acc = line[acc_index]
    dp_model_map[dp][model] = acc

model_acc_map = {}
for m in models:
    model_acc_map[m] = []

for dp in dps:
    for m in models:
        val = dp_model_map[dp][m]
        model_acc_map[m].append(val)

dest_dir = "../acc_files/microbe_pca"
for m in models:
    fstring = ",".join(model_acc_map[m])
    with open(f"{dest_dir}/{m}_microbe_accs_for_pca.txt", "w") as fh:
        fh.write(fstring)

