import json


base_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions"
json_path = f"{base_dir}/pdb_motif_prediction_data.json"

models = [
    "ContextFold",
    "ContraFold",
    "EternaFold",
    "IPKnot",
    "MXFold",
    "MXFold2",
    "Neuralfold",
    "NUPACK",
    "pKnots",
    "RNAFold",
    "RNAStructure",
    "Simfold",
    "SPOT-RNA"
]

print("Loading data")
with open(json_path) as fh:
    data = json.load(fh)

new_data = {}

print(f"Loaded {len(data):,} datapoints\n")

removed = 0
for dp, items in data.items():
    seq = items["sequence"]
    if len(seq) > 200:
        removed += 1
    else:
        new_data[dp] = items


print(f"Removed {removed:,} datapoints. There are {len(new_data):,} datapoints remaining")

print("Writing file")
with open(f"{base_dir}/pdb_motif_prediction_data_trimmed.json", "w") as fh:
    json.dump(new_data, fh)
