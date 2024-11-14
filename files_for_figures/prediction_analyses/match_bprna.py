import os, shutil


import pandas as pd


def get_file_loc(model):
    return f"{bprna_loc}/{model}_master_1_lenience.txt"

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
all_pred_file = open(f"{all_pred_dir}/bprna_master_file.txt")
data = all_pred_file.readlines()
all_pred_file.close()
data.pop(0)

model_count = len(models)
dp_counts = {}

for d in data:
    d = d.split(", ")
    name = d[2]
    try:
        dp_counts[name] += 1
    except KeyError:
        dp_counts[name] = 1


matched_dps = []
overly_matched = []
counts = []

for dp, count in dp_counts.items():
    counts.append(count)
    if count >= model_count:
        matched_dps.append(dp)
    if count > model_count:
        overly_matched.append(dp)

print(f"There are {len(matched_dps)} datapoints covered by every model")
print(f"Therae are {len(overly_matched)} datapoints that show up more than {model_count} times")
print(f"Highest dp recurrence: {max(counts)}")
print(f"Lowest dp recurrence: {min(counts)}")
print(f"Average recurrence: {sum(counts) / len(counts)}")

print("Assembling and writing matched set")

matched_set_file = open(f"{all_pred_dir}/bprna_matched_set.txt", "w")
for d in data:
    name = d.split(", ")[2]
    if name in matched_dps:
        matched_set_file.write(d)

matched_set_file.close()
print("Done!")
