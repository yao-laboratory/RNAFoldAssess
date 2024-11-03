import os, shutil

import pandas as pd


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

all_pred_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions"
all_pred_path = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions/crystal_master_file.txt"

with open(all_pred_path) as fh:
    data = fh.readlines()

model_count = len(models)
dp_counts = {}

data.pop(0)
for d in data:
    d = d.split(", ")
    model = d[0]
    name = d[1]
    if model == "RandomPredictor":
        continue
    try:
        dp_counts[name] += 1
    except KeyError:
        dp_counts[name] = 1


matched_dps = []
overly_matched = []
counts = []

matched_dps = []
overly_matched = []
counts = []

for dp, count in dp_counts.items():
    counts.append(count)
    if count >= model_count:
        matched_dps.append(dp)
    if count > model_count:
        overly_matched.append(dp)

print(f"There are a total of {len(data)} datapoints")
print(f"There are {len(matched_dps)} datapoints covered by every model")
print(f"Therae are {len(overly_matched)} datapoints that show up more than {model_count} times")
print(f"Highest dp recurrence: {max(counts)}")
print(f"Lowest dp recurrence: {min(counts)}")
print(f"Average recurrence: {sum(counts) / len(counts)}")

print("Assembling and writing matched set")

matched_set_file = open(f"{all_pred_dir}/pdb_matched_set.txt", "w")
for d in data:
    name = d.split(", ")[1]
    if name in matched_dps:
        matched_set_file.write(d)

matched_set_file.close()
print("Done!")
