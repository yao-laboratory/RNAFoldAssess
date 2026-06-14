import os, shutil


completed_path = "/work/yesselmanlab/ewhiting/outputs/ribonanza"
script_path = "/home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/canonize_chem_map_preds"

completed_dps = []
for file in os.listdir(completed_path):
    if ".dbn" not in file:
        continue

    dp = file.split(".")[0]
    completed_dps.append(dp)

fasta_dir = f"/mnt/nrdstor/yesselmanlab/ewhiting/data/fasta_files/ribonanza"

fstring = ""
os.mkdir("/scratch/neuralfold")
for f in os.listdir(fasta_dir):
    if ".fasta" not in f:
        continue
    dp = f.split(".")[0]
    if dp not in completed_dps:
        shutil.copy(f"{fasta_dir}/{f}", f"/scratch/neuralfold/{f}")
        fstring += f"{f}\n"

with open(f"{script_path}/fastas_todo.txt", "w") as fh:
    fh.write(fstring)

