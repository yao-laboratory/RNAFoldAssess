import os

import numpy as np


pred_location = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions"
matched_pred_file = f"{pred_location}/bprna_matched_set.txt"

with open(matched_pred_file) as fh:
    data = fh.readlines()

models = set()

dp_sen_map = {}
dp_ppv_map = {}
dp_f1_map = {}

sens = []
ppvs = []
f1s = []

print("Assembling prediction stats")
for d in data:
    d = d.split(", ")
    models.add(d[1])
    name = d[2]
    seq = d[3]
    stc = d[4]
    sens.append(float(d[6]))
    ppvs.append(float(d[7]))
    f1s.append(float(d[8].strip()))
    for mp_map in [dp_sen_map, dp_ppv_map, dp_f1_map]:
        mp_map[name] = {"hard": [], "easy": [], "other": [], "sequence": seq, "structure": stc}


print("Calculating quartiles")

s_quartiles = np.percentile(sens, [25, 50, 75])
p_quartiles = np.percentile(ppvs, [25, 50, 75])
f_quartiles = np.percentile(f1s, [25, 50, 75])

print(f"(Sensitivity) First quartile: {s_quartiles[0]}")
print(f"(Sensitivity) Second quartile (50th percentile/Median): {s_quartiles[1]}")
print(f"(Sensitivity) Third quartile: {s_quartiles[2]}")
print(f"(Sensitivity) There are {sens.count(0.0)} zeroes of {len(sens)}")
print()

print(f"(PPV) First quartile: {p_quartiles[0]}")
print(f"(PPV) Second quartile (50th percentile/Median): {p_quartiles[1]}")
print(f"(PPV) Third quartile: {s_quartiles[2]}")
print(f"(PPV) There are {ppvs.count(0.0)} zeroes of {len(ppvs)}")
print()

print(f"(F1) First quartile: {f_quartiles[0]}")
print(f"(F1) Second quartile (50th percentile/Median): {f_quartiles[1]}")
print(f"(F1) Third quartile: {f_quartiles[2]}")
print(f"(F1) There are {f1s.count(0.0)} zeroes of {len(f1s)}")
print()


report_base = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions/bprna_seps"
stats = {
    "Sensitivity": {"quartiles": s_quartiles, "dp_map": dp_sen_map},
    "PPV": {"quartiles": p_quartiles, "dp_map": dp_ppv_map},
    "F1": {"quartiles": f_quartiles, "dp_map": dp_f1_map}
}


print("Assembling good/bad predictions")
for line in data:
    d = line.split(", ")
    model = d[1]
    name = d[2]
    evals = {
        "Sensitivity": float(d[6]),
        "PPV": float(d[7]),
        "F1": float(d[8].strip()),
    }

    for stat, value in evals.items():
        quartiles = stats[stat]["quartiles"]
        dp_map = stats[stat]["dp_map"]
        if value <= quartiles[0]:
            # This is a hard datapoint
            dp_map[name]["hard"].append(model)
        elif value >= quartiles[2]:
            # This is an easy datapoint
            dp_map[name]["easy"].append(model)
        else:
            # This is a regular datapoint
            dp_map[name]["other"].append(model)



for stat in stats:
    easy_report = f"{report_base}/{stat}_bprna_easy.txt"
    hard_report = f"{report_base}/{stat}_bprna_hard.txt"
    all_others = f"{report_base}/{stat}_bprna_others.txt"
    stats[stat]["easy"] = open(easy_report, "w")
    stats[stat]["hard"] = open(hard_report, "w")
    stats[stat]["other"] = open(all_others, "w")

print("Assembling easy/hard datapoint reports")
for stat in stats:
    dp_map = stats[stat]["dp_map"]
    easy_report = stats[stat]["easy"]
    hard_report = stats[stat]["hard"]
    other_report = stats[stat]["other"]
    for dp in dp_map:
        seq = dp_map[dp]["sequence"]
        stc = dp_map[dp]["structure"]
        line = f"{dp}, {seq}, {stc}\n"
        easy_count = len(dp_map[dp]["easy"])
        hard_count = len(dp_map[dp]["hard"])
        if easy_count >= len(models):
            easy_report.write(line)
        elif hard_count >= len(models):
            hard_report.write(line)
        else:
            other_report.write(line)



for stat in stats:
    for ftype in ["easy", "hard", "other"]:
        stats[stat][ftype].close()

