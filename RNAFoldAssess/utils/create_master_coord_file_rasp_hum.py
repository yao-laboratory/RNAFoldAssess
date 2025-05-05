import os, sys, ast

args = sys.argv
given_chromosome = args[1]

legit_chromosomes = [
    "chr10",
    "chr11",
    "chr12",
    "chr13",
    "chr14",
    "chr15",
    "chr16",
    "chr17",
    "chr18",
    "chr19",
    "chr1",
    "chr20",
    "chr21",
    "chr22",
    "chr2",
    "chr3",
    "chr4",
    "chr5",
    "chr6",
    "chr7",
    "chr8",
    "chr9",
    "chrX",
    "chrY"
]

if given_chromosome not in legit_chromosomes:
    print(f"ERROR: {given_chromosome} not in allowed chromosomes")
    sys.exit()

coord_dir = "/common/yesselmanlab/ewhiting/data/rasp_data/human/coordinate_files"

files = [f for f in os.listdir(coord_dir) if f.endswith("_coords.txt") and f.startswith(given_chromosome)]

master_file = f"{coord_dir}/chromosome_{given_chromosome}.coords"

master_data = ""
for f in files:
    with open(f"{coord_dir}/{f}") as fh:
        data = fh.read().strip()
    exon_name = f.split("_coords.txt")[0]
    master_data += f"{exon_name}\n"
    if given_chromosome == "chr17":
        data = data.replace("][", "],[")
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

# Chromosome files are like "chr17_ENSE00000360905_coords.txt"
# Chromosomes:
# chr10
# chr11
# chr12
# chr13
# chr14
# chr15
# chr16
# chr17
# chr18
# chr19
# chr1
# chr20
# chr21
# chr22
# chr2
# chr3
# chr4
# chr5
# chr6
# chr7
# chr8
# chr9
# chrX
# chrY
