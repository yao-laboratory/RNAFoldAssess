import os


master_file = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions/rasp_microbe_master_predictions.txt"

with open(master_file) as fh:
    lines = [d.split(", ") for d in fh.readlines()]


model_index = 0
dp_index = 1
acc_index = 4

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

print("Building dp map")
all_dps = set()
for line in lines:
    dp = line[dp_index]
    all_dps.add(dp)

dp_map = {}
for dp in all_dps:
    dp_map[dp] = {}
    for m in models:
        dp_map[dp][m] = ""


print(f"Assembling acc files")
for line in lines:
    dp = line[dp_index]
    m = line[model_index]
    acc = line[acc_index]
    dp_map[dp][m] = acc

model_accs = {}
for m in models:
    model_accs[m] = []

for _dp, acc_info in dp_map.items():
    for m, acc in acc_info.items():
        model_accs[m].append(acc)

dest_dir = "../acc_files/microbe_pca"
for m in models:
    fstring = ",".join(model_accs[m])
    with open(f"{dest_dir}/{m}_microbe_accs_for_pca.txt", "w") as fh:
        fh.write(fstring)
