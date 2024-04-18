import os


reference = sorted(set("ACGU"))

base_dir = "/common/yesselmanlab/ewhiting/data/bprna/dbnFiles"
destination_dir = f"{base_dir}/filtered"
files = [f for f in os.listdir(base_dir) if f.endswith(".dbn")]
len_files = len(files)

all_seqs = []
counter = 0
for ff in files:
    if counter % 250 == 0:
        print(f"Working {counter} of {len_files}")
    f = open(f"{base_dir}/{ff}")
    seq = f.readlines()[3].strip()
    f.close()
    alphabet = set(seq)
    for s in seq:
        if s not in reference:
            break
        else:
            cmd = f"cp {base_dir}/{ff} {destination_dir}/{ff}"
            os.system(cmd)
    counter += 1

