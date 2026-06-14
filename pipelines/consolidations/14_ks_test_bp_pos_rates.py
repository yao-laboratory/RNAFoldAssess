import os

import matplotlib.pyplot as plt
import seaborn as sns



base_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions"
matched_set = f"{base_dir}/chemical_mapping_matched_set.txt"

with open(matched_set) as fh:
    lines = [line.strip().split(", ") for line in fh.readlines()]

print("Getting datapoints")
dp_map = {}
for line in lines:
    dp = line[2]
    seq = line[3]
    dp_map[dp] = {"sequence": seq, "positions": {}}


print(f"There are {len(dp_map)} data points")
print("Building position map")
for dp in dp_map:
    seq = dp_map[dp]["sequence"]
    for i in range(len(seq)):
        dp_map[dp]["positions"][i] = 0

print("Counting positives")
for line in lines:
    dp = line[2]
    pred = line[4]
    for i in range(len(pred)):
        nt = pred[i]
        if nt in "()":
            dp_map[dp]["positions"][i] += 1

print("Getting positive rate")
for dp in dp_map:
    for pos in dp_map[dp]["positions"]:
        dp_map[dp]["positions"][pos] /= 13

rates = []
for dp in dp_map:
    for pos in dp_map[dp]["positions"]:
        rates.append(dp_map[dp]["positions"][pos])


