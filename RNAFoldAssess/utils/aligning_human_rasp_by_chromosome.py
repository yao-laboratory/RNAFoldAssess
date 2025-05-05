import json, os, sys

args = sys.argv
given_chromosome = args[1]

acceptable_chromosomes = [f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"]
if given_chromosome not in acceptable_chromosomes:
    print(f"Unrecognized chromosome for human: {given_chromosome}. Must be one of {acceptable_chromosomes}")
    sys.exit()

# Example endfile for this script:
# file name: chromosome_chr1_ENST00000413769_dps_to_assemble.txt
# contents:
# chromosome_chr1_number_69100 - [88983946, 88983947]


gff_loc = "/common/yesselmanlab/ewhiting/data/rasp_data/human/hg38.gff3"
json_dir = "/common/yesselmanlab/ewhiting/data/rasp_data/human/processed"
dest_dir = "/common/yesselmanlab/ewhiting/data/rasp_data/human/assemble_files"
files = [f for f in os.listdir(json_dir) if f.endswith(".json")]

datapoints = []

print("Loading datapoints from JSON files")
for f in files:
    with open(f"{json_dir}/{f}") as ff:
        datapoints += json.load(ff)


print("Reading genome file")

with open(gff_loc) as gf:
    gff_data = [d.split("\t") for d in gf.readlines()]

exon_lines = []
for gd in gff_data:
    if gd[0] == given_chromosome and gd[2] == "exon":
        exon_lines.append(gd)

print(f"There are {len(exon_lines)} exon lines")
exon_data = {}
exon_coords = {}
dp_map = {}

for dp in datapoints:
    chromosome = dp["name"].split("_")[1]
    if chromosome != given_chromosome:
        continue
    exon_data[chromosome] = {}
    exon_coords[chromosome] = {}
    try:
        dp_map[chromosome].append(dp)
    except KeyError:
        dp_map[chromosome] = [dp]

print(f"Found {len(exon_data.keys())} chromosomes")

if len(dp_map) == 0:
    print(f"No datapoints found for {given_chromosome}")
    sys.exit()

for line in exon_lines:
    chromosome = line[0]
    if chromosome != given_chromosome:
        break
    exon_info = line[8]
    # Example:
    # Parent=transcript:ENST00000456328;Name=ENSE00002234944;constitutive=0;ensembl_end_phase=-1;ensembl_phase=-1;exon_id=ENSE00002234944;rank=1;version=1\n
    parent = exon_info.split(";")[0].split(":")[1]
    try:
        exon_data[chromosome][parent].append(
            [
                int(line[3]),
                int(line[4])
            ]
        )
    except KeyError:
        exon_data[chromosome][parent] = [
            [
                int(line[3]),
                int(line[4])
            ]
        ]

all_keys = list(exon_data.keys())
for ch in exon_data:
    print(f"{ch} has {len(exon_data[ch])} exon lines")
    print(f"{ch} has {len(dp_map[ch])} datapoints")
    print()

for ch in exon_data:
    data = exon_data[ch]
    for k in data:
        ranges = data[k]
        all_coords = []
        for start, end in ranges:
            all_coords += [i for i in range(start, end)]
        exon_coords[k] = all_coords

print("Assembling datapoints")

counter = 0
for ch in dp_map:
    print(f"Working {ch}")
    dps = dp_map[ch]
    for dp in dps:
        counter += 1
        if counter % 350 == 0:
            print(f"Working {counter} of {len(dps)}")
        dp_coords = [int(i) for i in dp["coordinates"]]
        for k in exon_coords:
            coords = exon_coords[k]
            if all(i in coords for i in dp_coords):
                f = open(f"{dest_dir}/chromosome_{given_chromosome}_{k}_dps_to_assemble.txt", "a")
                line = f"{dp['name']} - {dp['coordinates']}\n"
                f.write(line)
