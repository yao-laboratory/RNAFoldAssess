import os

from RNAFoldAssess.utils.secondary_structure_tools import SecondaryStructureTools
from rna_secstruct import SecStruct

base_dir = "/common/yesselmanlab/ewhiting/data/bprna/dbnFiles"
destination_dir = "/common/yesselmanlab/ewhiting/data/bprna/data_with_fe"
dbn_files = [f for f in os.listdir(base_dir) if f.endswith(".dbn")]
files_count = len(dbn_files)

fe_file = open(f"{destination_dir}/data.txt", "w")

counter = 0
for df in dbn_files:
    if counter % 250 == 0:
        print(f"Working {counter} of {files_count}")
    name = df.split(".")[0]
    f = open(f"{base_dir}/{df}")
    data = f.readlines()
    # For testing
    data = data[:10]
    f.close()
    data = [d.strip() for d in data]
    seq = data[3]
    stc = data[4]
    fe = SecondaryStructureTools.get_free_energy(seq, stc)
    line = f"{name}, {seq}, {stc}, {fe}\n"
    fe_file.write(line)
    counter += 1

fe_file.close()
