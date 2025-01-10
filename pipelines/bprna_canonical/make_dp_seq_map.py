import os


dbn_path = "/work/yesselmanlab/ewhiting/data/bprna/dbnFiles"
all_dbns = [f for f in os.listdir(dbn_path) if ".dbn" in f]

dp_index = "/work/yesselmanlab/ewhiting/data/bprna/"
index_file = open(f"{dp_index}/dp_index.txt", "w")

for dbn_file in all_dbns:
    dp_name = dbn_file.split(".")[0]
    with open(f"{dbn_path}/{dbn_file}") as fh:
        data = fh.readlines()
    seq = data[3].strip()
    index_file.write(f"{seq} {dp_name}\n")

index_file.close()
