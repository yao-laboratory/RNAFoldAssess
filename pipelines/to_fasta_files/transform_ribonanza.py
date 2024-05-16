import os


ribo_data_csv = "/common/yesselmanlab/ewhiting/data/ribonanza/rmdb_data.v1.3.0.csv"
destination_dir = "/common/yesselmanlab/ewhiting/data/fasta_files/ribonanza"
f = open(ribo_data_csv)
data = f.readlines()
f.close()
# Get rid of headers
data.pop(0)
data = [d.split(",") for d in data]
r1_index = 7

for d in data:
    name = d[0]
    seq = d[1]
    with open(f"{destination_dir}/{name}.fasta", "w") as f:
        f.write(f">{name} en=0.00\n{seq}")

