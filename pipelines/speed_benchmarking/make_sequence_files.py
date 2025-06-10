import os, shutil


dbn_file_path = "/work/yesselmanlab/ewhiting/data/bprna/speed_dataset"
dbn_files = os.listdir(dbn_file_path)
destination = "/work/yesselmanlab/ewhiting/data/bprna/speed_dataset_fasta"
os.mkdir(destination)

for df in dbn_files:
    with open(f"{dbn_file_path}/{df}") as fh:
        dbn_data = fh.readlines()

    name = df.split(".")[0]
    seq = dbn_data[3].strip()
    fasta_string = f">{name}\n{seq}"

    with open(f"{destination}/{name}.fasta", "w") as fh:
        fh.write(fasta_string)
