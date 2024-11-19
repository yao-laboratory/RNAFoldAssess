import json, os, sys

args = sys.argv
given_chromosome = args[1]

acceptable_chromosomes = ["U00096.2"]
if given_chromosome not in acceptable_chromosomes:
    print(f"Unrecognized chromosome for ecoli: {given_chromosome}. Must be one of {acceptable_chromosomes}")
    sys.exit()

gff_loc = "/common/yesselmanlab/ewhiting/data/rasp_data/ecoli/ecoli.gff3"
json_dir = "/common/yesselmanlab/ewhiting/data/rasp_data/processed/ecoli/round_2"
dest_dir = "/common/yesselmanlab/ewhiting/data/rasp_data/ecoli"
files = os.listdir(json_dir)

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
    # ID=exon-b4414-1;Parent=rna-b4414;Dbxref=ASAP:ABE-0047239,EcoGene:EG31135;Note=identified in a large scale screen;gbkey=ncRNA;gene=tff;locus_tag=b4414;product=no     vel sRNA%2C function unknown
    s = exon_info.index("=")
    e = exon_info.index(";")
    parent = exon_info[s+1:e]
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

