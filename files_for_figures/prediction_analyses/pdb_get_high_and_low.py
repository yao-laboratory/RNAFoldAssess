import os

import numpy as np


base_loc = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions"
all_pdb_preds_file = f"{base_loc}/pdb_matched_set.txt"

with open(all_pdb_preds_file) as fh:
    data = fh.readlines()

sen_index = 5
ppv_index = 6
f1_index = 7

data = [d.split(", ") for d in data]
data = [d for d in data if d[0] != "RandomPredictor"]

all_sens = [float(d[sen_index]) for d in data]
quartiles = np.percentile(all_sens, [25, 50, 75])
print(f"(Sensitivity) First quartile: {quartiles[0]}")
print(f"(Sensitivity) Second quartile (50th percentile/Median): {quartiles[1]}")
print(f"(Sensitivity) Third quartile: {quartiles[2]}")
print(f"(Sensitivity) There are {all_sens.count(0.0)} zeroes of {len(all_sens)}")
print()

all_ppvs = [float(d[ppv_index]) for d in data]
quartiles = np.percentile(all_ppvs, [25, 50, 75])
print(f"(PPV) First quartile: {quartiles[0]}")
print(f"(PPV) Second quartile (50th percentile/Median): {quartiles[1]}")
print(f"(PPV) Third quartile: {quartiles[2]}")
print(f"(PPV) There are {all_ppvs.count(0.0)} zeroes of {len(all_ppvs)}")
print()

all_f1s = [float(d[f1_index].strip()) for d in data]
quartiles = np.percentile(all_f1s, [25, 50, 75])
print(f"(F1) First quartile: {quartiles[0]}")
print(f"(F1) Second quartile (50th percentile/Median): {quartiles[1]}")
print(f"(F1) Third quartile: {quartiles[2]}")
print(f"(F1) There are {all_f1s.count(0.0)} zeroes of {len(all_f1s)}")


easy_report_fasta = f"{base_loc}/pdb_easy.fasta"
hard_report_fasta = f"{base_loc}/pdb_hard.fasta"
background = f"{base_loc}/pdb_background.fasta"

hard_structures = f"{base_loc}/pdb_hard_structures.txt"

dp_map = {}
for d in data:
    name = d[1]
    dp_map[name] = {"easy": 0, "hard": 0}

for d in data:
    name = d[1]
    ppv = float(d[ppv_index])
    if ppv == 0.0:
        dp_map[name]["hard"] += 1
    elif ppv == 1.0:
        dp_map[name]["easy"] += 1

easy_dps = []
hard_dps = []

for dp, counts in dp_map.items():
    if counts["easy"] == 12:
        easy_dps.append(dp)
    elif counts["hard"] == 13:
        hard_dps.append(dp)

print(f"There are {len(easy_dps)} easy datapoints")
for ed in easy_dps:
    print(f"\t{ed}")
print(f"There are {len(hard_dps)} hard datapoints")

fasta_string = ""
structure_string = ""

completed_dps = []
found_structures = []
for d in data:
    name = d[1]
    if name in hard_dps and name not in completed_dps:
        completed_dps.append(name)
        seq = d[2]
        true_structure = d[3]
        fasta_string += f">{name}\n{seq}\n"
        if true_structure not in found_structures:
            structure_string += f"{true_structure}\n"
            found_structures.append(true_structure)

with open(hard_report_fasta, "w") as fh:
    fh.write(fasta_string.strip())

with open(hard_structures, "w") as fh:
    fh.write(structure_string.strip())


found_dps = []
fasta_string = ""
for d in data:
    name = d[1]
    if name not in hard_dps and name not in found_dps:
        found_dps.append(name)
        seq = d[2]
        fasta_string += f">{name}\n{seq}\n"

with open(f"{base_loc}/background_pdb.fasta", "w") as fh:
    fh.write(fasta_string.strip())
