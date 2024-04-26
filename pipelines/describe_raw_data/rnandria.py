import os

from RNAFoldAssess.models import DataPoint

base_path = "/common/yesselmanlab/ewhiting/data/rnandria/rnandria_data_JSON/processed"
pri_miRNA = f"{base_path}/pri_miRNA_datapoints.json"
human_mRNA = f"{base_path}/human_mRNA_datapoints.json"

pri_dps = DataPoint.factory(pri_miRNA)
human_dps = DataPoint.factory(human_mRNA)

dataset_name = "rnandria"
destination_dir = "/common/yesselmanlab/ewhiting/data/descriptions"

pri_seq_lengths = []
pri_seq_gc_contents = []
human_seq_lengths = []
human_seq_gc_contents = []
all_seq_lengths = []
all_seq_gc_contents = []


pri_len_file = f"{destination_dir}/{dataset_name}_pri_lengths.txt"
pri_gc_file = f"{destination_dir}/{dataset_name}_pri_gc_content.txt"
human_len_file = f"{destination_dir}/{dataset_name}_human_lengths.txt"
human_gc_file = f"{destination_dir}/{dataset_name}_human_gc_content.txt"
all_len_file = f"{destination_dir}/{dataset_name}_all_lengths.txt"
all_gc_file = f"{destination_dir}/{dataset_name}_all_gc_content.txt"

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

print("Checking pri")
for dp in pri_dps:
    slan = len(dp.sequence)
    gc = get_gc_content(dp.sequence)
    pri_seq_lengths.append(slan)
    all_seq_lengths.append(slan)
    pri_seq_gc_contents.append(gc)
    all_seq_gc_contents.append(gc)

print("Checking human")
for dp in human_dps:
    slan = len(dp.sequence)
    gc = get_gc_content(dp.sequence)
    human_seq_lengths.append(slan)
    all_seq_lengths.append(slan)
    human_seq_gc_contents.append(gc)
    all_seq_gc_contents.append(gc)

print("Writing files")
f = open(pri_len_file, "w")
for l in pri_seq_lengths:
    f.write(f"{l}\n")
f.close()

f = open(all_len_file, "w")
for l in all_seq_lengths:
    f.write(f"{l}\n")
f.close()

f = open(human_len_file, "w")
for l in human_seq_lengths:
    f.write(f"{l}\n")
f.close()

f = open(pri_gc_file, "w")
for g in pri_seq_gc_contents:
    f.write(f"{g}\n")
f.close()

f = open(human_gc_file, "w")
for g in human_seq_gc_contents:
    f.write(f"{g}\n")
f.close()

f = open(all_gc_file, "w")
for g in all_seq_gc_contents:
    f.write(f"{g}\n")
f.close()
