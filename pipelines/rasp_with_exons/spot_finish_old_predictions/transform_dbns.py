import os

base_dir = "/common/yesselmanlab/ewhiting/spot_outputs/rasp"

species = ["covid", "ecoli", "hiv"]

for s in species:
    print(f'Working {s}')
    dbn_path = f"{base_dir}/{s}/dbn_files"
    dbn_files = [f for f in os.listdir(dbn_path) if f.endswith(".dbn")]
    for df in dbn_files:
        with open(f"{dbn_path}/{df}") as fh:
            lines = fh.readlines()
        dbn_string = lines[2].strip()
        dbn_string = list(dbn_string)
        for i, nt in enumerate(dbn_string):
            if nt not in ".()":
                dbn_string[i] = "."
        dbn_string = "".join(dbn_string)
        fstring = lines[0] + lines[1] + dbn_string + "\n"
        with open(f"{dbn_path}/{df}", "w") as fh:
            fh.write(fstring)
