import os


matched_file = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions/bprna_matched_set.txt"

models = [
    "ContextFold",
    "ContraFold",
    "EternaFold",
    "IPKnot",
    "NeuralFold",
    "NUPACK",
    "RNAFold",
    "RNAStructure",
    "pKnots",
    "Simfold",
    "MXFold",
    "MXFold2",
    "SPOT-RNA"
]

dest_dir = "/home/yesselmanlab/ewhiting/RNAFoldAssess/files_for_figures/bprna"


model_map = {}

for m in models:
    model_map[m] = {"sens": [], "ppv": [], "f1": []}

# 6, 7, 8 

with open(matched_file) as fh:
    data = [d.split(", ") for d in fh.readlines()]

counter = 0
len_data = len(data)
for d in data:
    counter += 1
    if counter % 1000 == 0:
        print(f"Working {counter} of {len_data}")
    model = d[1]
    if model == "RandomPredictor":
        continue
    s = float(d[6])
    p = float(d[7])
    f = float(d[8])
    model_map[model]["sens"].append(s)
    model_map[model]["ppv"].append(p)
    model_map[model]["f1"].append(f)


for m, stats in model_map.items():
    for stat in ["sens", "ppv", "f1"]:
        values = stats[stat]
        with open(f"{dest_dir}/{m}_{stat}.txt", "w") as fh:
            fh.write(",".join([str(i) for i in values]))
