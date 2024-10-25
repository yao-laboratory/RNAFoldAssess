import os


dp_file_path = "/common/yesselmanlab/ewhiting/ss_deeplearning_data/data"
u_destination = "/common/yesselmanlab/ewhiting/neuralfold_scripts/missing_ydata_u.txt"
v_destination = "/common/yesselmanlab/ewhiting/neuralfold_scripts/missing_ydata_v.txt"

approved_chorots = [
    "C014U",
    "C014V"
]

with open("../NeuralFold_missing_dps.txt") as r:
    missing_dps = [line.strip() for line in r.readlines()]


u_missing_ydata = [md for md in missing_dps if md[:5] == "C014U"]
v_missing_ydata = [md for md in missing_dps if md[:5] == "C014V"]

with open(u_destination, "w") as fh:
    for md in u_missing_ydata:
        fh.write(f"{md}.fasta\n")

with open(v_destination, "w") as fh:
    for md in v_missing_ydata:
        fh.write(f"{md}.fasta\n")
