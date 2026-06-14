import os

from RNAFoldAssess.models.scorers import *


low = 0.3889
high = 0.8571

base_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis"
src_dir = f"{base_dir}/latest/all_predictions"
dest_dir = f"{base_dir}/consolidated"

ref_file = f"{src_dir}/bprna_master_file_0.txt"

f1_index = 9

print("Opening predictions")
with open(ref_file) as fh:
    lines = [line.split(", ") for line in fh.readlines()]
lines.pop(0)

dps = set([(line[3], line[4], line[5]) for line in lines])
dp_acc_map = {}

print("Creating dp_map")
for dp in dps:
    name = dp[0]
    seq = dp[1]
    stc = dp[2]
    stc = CanonicalBasePairScorer.transform_structure(stc, seq)
    dp_acc_map[name] = {'sequence': seq, 'structure': stc, 'high': [], 'low': []}

print("Assigning hi/low scores")
for line in lines:
    dp = line[3]
    f1 = float(line[f1_index])
    if f1 <= low:
        dp_acc_map[dp]['low'].append(f1)
    elif f1 >= high:
        dp_acc_map[dp]['high'].append(f1)

print("Counting hi/low scores")
hard_dps = []
easy_dps = []
for dp, values in dp_acc_map.items():
    c_high = len(values["high"])
    c_low = len(values["low"])
    if c_high == 13:
        easy_dps.append(
            f"{dp}, {values['sequence']}, {values['structure']}"
        )
    elif c_low == 13:
        hard_dps.append(
            f"{dp}, {values['sequence']}, {values['structure']}"
        )

with open(f"{dest_dir}/bprna_easy_cases.txt", "w") as fh:
    fh.write("\n".join(easy_dps))

with open(f"{dest_dir}/bprna_hard_cases.txt", "w") as fh:
    fh.write("\n".join(hard_dps))

print("Done")
