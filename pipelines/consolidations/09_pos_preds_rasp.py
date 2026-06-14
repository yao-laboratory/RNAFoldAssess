import os

import matplotlib.pyplot as plt
import seaborn as sns


matched_base = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions"
matched_human = f"{matched_base}/rasp_matched_set_human.txt"
matched_ara = f"{matched_base}/rasp_ara_matched_set.txt"
matched_microbe = f"{matched_base}/rasp_microbe_matched_set.txt"

lines = []
for matched_path in [matched_human, matched_ara, matched_microbe]:
    with open(matched_path) as fh:
        lines += [line.strip().split(", ") for line in fh.readlines()]

print("Getting datapoints")
dp_map = {}
for line in lines:
    dp = line[1]
    seq = line[2].replace("T", "U")
    dp_map[dp] = {"sequence": seq, "positions": {}}

print(f"There are {len(dp_map)} data points")
print("Building position map")
for dp in dp_map:
    seq = dp_map[dp]["sequence"]
    for i in range(len(seq)):
        dp_map[dp]["positions"][i] = 0

print("Counting positives")
for line in lines:
    dp = line[1]
    pred = line[3]
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
        rates.append(
            dp_map[dp]["positions"][pos]
        )


sns.kdeplot(rates, fill=True, cut=0)
plt.xlabel("Rate")
plt.ylabel("Density")
plt.title("KDE Plot of Base Pair Prediction Position Rates (RASP)")

plt.savefig("bp_prediction_position_rate_rasp.jpg", format="jpeg", dpi=300, bbox_inches="tight")
plt.close()


