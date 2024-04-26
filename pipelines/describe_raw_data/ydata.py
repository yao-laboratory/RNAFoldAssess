import os

from RNAFoldAssess.models import DataPoint


approved_chorots = [
    "C014G",
    "C014H",
    "C014I",
    "C014J",
    "C014U",
    "C014V"
]

dp_file_path = "/common/yesselmanlab/ewhiting/ss_deeplearning_data/data"
data_point_files = os.listdir(dp_file_path)

datapoints = []
for dpf in data_point_files:
    cohort = dpf.split(".")[0]
    if cohort not in approved_chorots:
        continue
    print(f"Loading data points from {cohort} cohort")
    dps = DataPoint.factory(f"{dp_file_path}/{dpf}", cohort)
    datapoints += dps

dataset_name = "ydata"
destination_dir = "/common/yesselmanlab/ewhiting/data/descriptions"

seq_lengths = []
seq_gc_contents = []
shape_method_count = 0
dms_method_count = 0

len_file = f"{destination_dir}/{dataset_name}_lengths.txt"
gc_file = f"{destination_dir}/{dataset_name}_gc_content.txt"

def get_gc_content(seq):
    seq = seq.strip().upper() # Just in case
    gs = seq.count("G")
    cs = seq.count("C")
    gc_count = gs + cs
    gc_count = float(gc_count)
    slen = float(len(seq))
    gc_content = gc_count / slen
    gc_content = round(gc_content, 6)
    return gc_content

for dp in datapoints:
    seq_lengths.append(len(dp.sequence))
    seq_gc_contents.append(get_gc_content(dp.sequence))

f = open(len_file, "w")
for l in seq_lengths:
    f.write(f"{l}\n")
f.close()

f = open(gc_file, "w")
for g in seq_gc_contents:
    f.write(f"{g}\n")
f.close()

