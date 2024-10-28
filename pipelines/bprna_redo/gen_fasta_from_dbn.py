import os, sys


print("Starting")
path_matches = []
for partition in range(0, 103):
    dbn_path = f"/work/yesselmanlab/ewhiting/data/bprna/dbnFiles_sep/part_{partition}"
    fasta_path = f"/work/yesselmanlab/ewhiting/data/bprna/fastaFiles_sep/part_{partition}"
    if not os.path.isdir(fasta_path):
        os.mkdir(fasta_path)
    path_matches.append(
        (dbn_path, fasta_path)
    )


for dbn_path, fasta_path in path_matches:
    print(f"Working in {dbn_path}")
    dbn_files = [f for f in os.listdir(dbn_path) if f.endswith(".dbn")]

    for dbn_file in dbn_files:
        with open(f"{dbn_path}/{dbn_file}") as fh:
            dbn_data = fh.readlines()
        name = dbn_file.replace(".dbn", "")
        seq = dbn_data[3].strip()
        fasta_data = f">{name}\n{seq}"
        with open(f"{fasta_path}/{name}.fasta", "w") as fh:
            fh.write(fasta_data)


print("Done")
