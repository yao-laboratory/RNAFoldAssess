import os


matched_file = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions/pdb_matched_set.txt"

models = [
    "ContextFold",
    "ContraFold",
    "EternaFold",
    "IPKnot",
    "Neuralfold",
    "NUPACK",
    "RNAFold",
    "RNAStructure",
    "pKnots",
    "Simfold",
    "MXFold",
    "MXFold2",
    "SPOT-RNA"
]

dest_dir = "/home/yesselmanlab/ewhiting/RNAFoldAssess/files_for_figures/pdb"


model_map = {}

for m in models:
    model_map[m] = {"sens": [], "ppv": [], "f1": []}

# 5, 6, 7

with open(matched_file) as fh:
    data = [d.split(", ") for d in fh.readlines()]

for d in data:
    model = d[0]
    if model == "RandomPredictor":
        continue
    s = float(d[5])
    p = float(d[6])
    f = float(d[7])
    model_map[model]["sens"].append(s)
    model_map[model]["ppv"].append(p)
    model_map[model]["f1"].append(f)


for m, stats in model_map.items():
    for stat in ["sens", "ppv", "f1"]:
        values = stats[stat]
        with open(f"{dest_dir}/{m}_{stat}.txt", "w") as fh:
            fh.write(",".join([str(i) for i in values]))
