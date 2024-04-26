import os

from RNAFoldAssess.models import DataPoint


ribo_data_csv = "/common/yesselmanlab/ewhiting/data/ribonanza/rmdb_data.v1.3.0.csv"
f = open(ribo_data_csv)
datapoints = f.readlines()
f.close()
# Get rid of headers
datapoints.pop(0)
datapoints = [d.split(",") for d in datapoints]

dataset_name = "ribonanza"
destination_dir = "/common/yesselmanlab/ewhiting/data/descriptions"

seq_lengths = []
seq_gc_contents = []

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

print("starting")

for dp in datapoints:
    seq = dp[1]
    seq_lengths.append(len(seq))
    seq_gc_contents.append(get_gc_content(seq))

print("writing")

f = open(len_file, "w")
for l in seq_lengths:
    f.write(f"{l}\n")
f.close()

f = open(gc_file, "w")
for g in seq_gc_contents:
    f.write(f"{g}\n")
f.close()

