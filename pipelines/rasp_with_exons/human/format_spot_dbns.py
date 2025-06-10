import os


dbn_dir = f"/common/yesselmanlab/ewhiting/spot_outputs/rasp/human/dbn_files"
dest_dir = f"{dbn_dir}/formatted"

files = [f for f in os.listdir(dbn_dir) if f.endswith(".dbn")]

def transform_dbn(dbn):
    dbn = dbn.replace("<", "(").replace(">", ")")

    dbn = list(dbn)
    for i in range(len(dbn)):
        if dbn[i] not in "().":
            dbn[i] = "."
    dbn = "".join(dbn)
    return dbn


for f in files:
    with open(f"{dbn_dir}/{f}") as fh:
        dbn_data = fh.readlines()
    
    dbn = dbn_data[2].strip()
    dbn = transform_dbn(dbn) + "\n"
    dbn_data[2] = dbn

    with open(f"{dest_dir}/{f}", "w") as fh:
        fh.write("".join(dbn_data))
