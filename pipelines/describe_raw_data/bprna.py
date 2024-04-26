import os

sequence_data_path = "/common/yesselmanlab/ewhiting/data/bprna/dbnFiles"

dbn_files = os.listdir(sequence_data_path)
dbn_files = [f for f in dbn_files if f.endswith("dbn")]

dataset_name = "bprna"
destination_dir = "/common/yesselmanlab/ewhiting/data/descriptions"

len_file = f"{destination_dir}/{dataset_name}_lengths.txt"
gc_file = f"{destination_dir}/{dataset_name}_gc_content.txt"

lf = open(len_file, "w")
gf = open(gc_file, "w")

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

counter = 0
for sf in dbn_files:
    if counter % 250 == 0:
        print(f"Working {counter}")
    data = open(f"{sequence_data_path}/{sf}")
    data = data.readlines()
    sequence = data[-1].strip()
    slen = len(sequence)
    gc = get_gc_content(sequence)
    lf.write(f"{slen}\n")
    gf.write(f"{gc}\n")
    counter += 1

lf.close()
gf.close()
