import os


base_dir = "/work/yesselmanlab/ewhiting/spot_outputs/ydata"
existing_uprds = f"{base_dir}/C014U"
existing_vprds = f"{base_dir}/C014V"

existing_preds = []

for f in os.listdir(existing_uprds):
    dp_name = f.split(".")[0]
    existing_preds.append(dp_name)

for f in os.listdir(existing_vprds):
    dp_name = f.split(".")[0]
    existing_preds.append(dp_name)

print(f"There are {len(existing_preds)} existing predictions")

fasta_base = "/work/yesselmanlab/ewhiting/reverse_experiment/fasta_files"
ufasta_files = f"{fasta_base}/C014U"
vfasta_files = f"{fasta_base}/C014V"

udps_todo = open("/work/yesselmanlab/ewhiting/spot_inputs/C014U_dps_todo.txt", "w")
for f in os.listdir(ufasta_files):
    name = f.split(".")[0]
    if name not in existing_preds:
        udps_todo.write(f"{name}\n")

udps_todo.close()

vdps_todo = open("/work/yesselmanlab/ewhiting/spot_inputs/C014V_dps_todo.txt", "w")
for f in os.listdir(vfasta_files):
    name = f.split(".")[0]
    if name not in existing_preds:
        vdps_todo.write(f"{name}\n")

vdps_todo.close()
