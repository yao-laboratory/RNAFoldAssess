import os, ast


csv_file = "/common/yesselmanlab/ewhiting/data/pdb_from_github/PDB-RNA.csv"

with open(csv_file) as fh:
    data = [d.strip() for d in fh.readlines()]

# Remove headers
data.pop(0)

# ~First, let's see if it's 0-indexed or 1-indexed~
# Data is 1-indexed for some reason
file_str = ""
for d in data:
    name = d.split(",")[0]
    seq = d.split(",")[1]
    length = int(d.split(",")[-1].strip())
    dbn = ["."] * length
    if "[]" not in d:
        bp_start = d.find('"[[')
        bp_end = d.find(']]"')
        bps = d[bp_start:bp_end+3]
        bps = ast.literal_eval(bps.replace('"', ""))
        for bp in bps:
            left_side = bp[0] - 1
            right_side = bp[1] - 1
            dbn[left_side] = "("
            dbn[right_side] = ")"
    dbn = "".join(dbn)
    file_str += f"{name}, {seq}, {dbn}\n"


with open("/common/yesselmanlab/ewhiting/data/pdb_from_github/processed.txt", "w") as fh:
    fh.write(file_str)

