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

print("Plotting rates")
rates = []
for dp in dp_map:
    for pos in dp_map[dp]["positions"]:
        rates.append(dp_map[dp]["positions"][pos])

# Plot as a bar plot (histogram)
import numpy as np
sns.histplot(rates, bins=14, kde=False)  # adjust bins as needed
plt.xlabel("Rate")
plt.ylabel("Count")
plt.title("Histogram of Base Pair Prediction Position Rates (in-vitro)")
plt.tight_layout()
plt.savefig("bp_prediction_position_rate_chem_map_bar2.jpg", format="jpeg", dpi=300, bbox_inches="tight")
plt.close()



