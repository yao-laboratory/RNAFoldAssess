# Don't run this with the rna_fold_assess conda environment
# Use nfold_env

import os, sys

partition = sys.argv[1]

fasta_dir = f"/scratch/partition_{partition}"
os.mkdir(fasta_dir)
dbn_path = f"/work/yesselmanlab/ewhiting/data/bprna/dbnFiles_sep/part_{partition}"
dbn_files = os.listdir(dbn_path)

print(f"Writing fasta files to {fasta_dir}")
for dbn_file in dbn_files:
    with open(f"{dbn_path}/{dbn_file}") as f:
        dbn_data = f.readlines()
    seq = dbn_data[3].strip()
    dbn = dbn_data[4].strip()
    name = dbn_file.split(".")[0]
    if len(seq) != len(dbn):
        continue
    fasta_string = f">{name}\n{seq}"
    with open(f"{fasta_dir}/{name}.fasta", "w") as ff:
        ff.write(fasta_string)

print("Starting predictions")
for f in os.listdir(fasta_dir):
    ncmd = f"/common/yesselmanlab/ewhiting//Neuralfold/NEURALfold.py test {fasta_dir}/{f}"
    output = f"/work/yesselmanlab/ewhiting/neuralfold_outputs/bprna"
    name = f.split(".")[0]
    cmd = f"python {ncmd} > {output}/{name}.dbn"
    os.system(cmd)
