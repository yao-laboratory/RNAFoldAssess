import os

import numpy as np

base_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis"
src_dir = f"{base_dir}/latest/all_predictions"
dest_dir = f"{base_dir}/consolidated"

ref_file = f"{src_dir}/bprna_master_file_0.txt"

f1_index = 9

with open(ref_file) as fh:
    lines = [line.split(", ") for line in fh.readlines()]

lines.pop(0)

f1s = [float(line[f1_index]) for line in lines]

q1 = np.percentile(f1s, 25)
q2 = np.percentile(f1s, 50)  # This is the median
q3 = np.percentile(f1s, 75)

print("Q1:", q1)
print("Median (Q2):", q2)
print("Q3:", q3)

# Q1: 0.3888888888888889
# Median (Q2): 0.6250000000000001
# Q3: 0.8571428571428571
