import os, shutil


dbn_file_path = "/work/yesselmanlab/ewhiting/data/bprna/dbnFiles"
dbn_files = os.listdir(dbn_file_path)
destination = "/work/yesselmanlab/ewhiting/data/bprna/speed_dataset"

min_length = 500
max_length = 1500

def acceptable_sequence(seq):
    lseq = len(seq)
    if lseq < min_length:
        return False
    
    if lseq > max_length:
        return False
    
    acceptable_sequence = "ACUG"
    uniq_seq = set(seq)
    for nt in uniq_seq:
        if nt not in acceptable_sequence:
            return False
    
    return True


candidate_files_found = 0

for dbn_file in dbn_files:
    file_path = f"{dbn_file_path}/{dbn_file}"
    with open(file_path) as fh:
        dbn_data = fh.readlines()

    seq = dbn_data[3].strip()

    if acceptable_sequence(seq):
        candidate_files_found += 1
        shutil.copy(file_path, f"{destination}/{dbn_file}")

    if candidate_files_found >= 100:
        break

