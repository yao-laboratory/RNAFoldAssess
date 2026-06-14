import os, shutil


script_path = "/mnt/nrdstor/yesselmanlab/ewhiting/spot_scripts/ribonanza"
completed_path = "/mnt/nrdstor/yesselmanlab/ewhiting/spot_outputs/ribonanza/fixed_title"

completed_dps = []
for file in os.listdir(completed_path):
    if ".ct" not in file:
        continue

    dp = file.split(".")[0]
    completed_dps.append(dp)


fasta_dir = f"/mnt/nrdstor/yesselmanlab/ewhiting/data/fasta_files/ribonanza"

fstring = ""
for f in os.listdir(fasta_dir):
    if ".fasta" not in f:
        continue
    
    dp = f.split(".")[0]
    if dp not in completed_dps:
        shutil.copy(f"{fasta_dir}/{f}", f"/scratch/{f}")
        fstring += f"{f}\n"

with open(f"{script_path}/fastas_todo.txt", "w") as fh:
    fh.write(fstring)
