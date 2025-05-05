import os, json, ast



coord_dir = "/common/yesselmanlab/ewhiting/data/rasp_data/human/coordinate_files"
# chromosomes = [f"chr{i}" for i in range(10, 23)] + ["chrX", "chrY"]
# For testing
chromosomes = ["chr17"]

for given_chromosome in chromosomes:
    print(f"Working chromosome {given_chromosome}")
    files = [f for f in os.listdir(coord_dir) if f.endswith("_coords.txt") and f.startswith(f"{given_chromosome}_")]

    master_file = f"{coord_dir}/chromosome_{given_chromosome}.coords"
    coord_files_to_remove = []
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
        # os.remove(f"{coord_dir}/{f}")
        coord_files_to_remove.append(f"{coord_dir}/{f}")


    with open(master_file, "w") as f:
        f.write(master_data)

    print(f"Done writing {given_chromosome}")
    for ff in coord_files_to_remove:
        os.remove(ff)
    
    print(f"Done deleting {given_chromosome}")

