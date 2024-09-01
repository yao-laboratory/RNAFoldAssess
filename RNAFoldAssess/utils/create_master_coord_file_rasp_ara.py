import os, sys, ast

args = sys.argv
given_chromosome = args[1]


coord_dir = "/common/yesselmanlab/ewhiting/data/rasp_data/ara-tha/coordinate_files"

files = [f for f in os.listdir(coord_dir) if f.endswith("_coords.txt") and f.startswith(given_chromosome)]

master_file = f"{coord_dir}/chromosome_{given_chromosome}.coords"

master_data = ""
for f in files:
    with open(f"{coord_dir}/{f}") as fh:
        data = fh.read().strip()
    exon_name = f.split("_coords.txt")[0]
    master_data += f"{exon_name}\n"
    data = ast.literal_eval(data)
    ranges = []
    for d in data:
        start = d[0]
        end = d[1]
        for i in range(start, end):
            ranges.append(str(i))
    master_data += ",".join(ranges)
    master_data += "\n"
    os.remove(f"{coord_dir}/{f}")


with open(master_file, "w") as f:
    f.write(master_data)
