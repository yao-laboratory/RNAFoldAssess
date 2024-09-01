import json, os


finished_points = [f.split("_")[0] for f in os.listdir("/common/yesselmanlab/ewhiting/data/rasp_data/ara-tha")]

gff_loc = "/common/yesselmanlab/ewhiting/data/rasp_data/ara-tha/TAIR10.gff3"
json_dir = "/common/yesselmanlab/ewhiting/data/rasp_data/processed/arabidopsis/round2"
dest_dir = "/common/yesselmanlab/ewhiting/data/rasp_data/ara-tha"
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
    if gd[2] == "exon":
        exon_lines.append(gd)

print(f"There are {len(exon_lines)} exon lines")
exon_data = {}
for line in exon_lines:
    exon_info = line[8]
    # Example:
    # Parent=transcript:AT1G01010.1;Name=AT1G01010.1.exon1;constitutive=1;ensembl_end_phase=1;ensembl_phase=-1;exon_id=AT1G01010.1.exon1;rank=1
    parent = exon_info.split(";")[0].split(":")[1]
    if parent in finished_points:
        continue
    try:
        exon_data[parent].append(
            [
                int(line[3]),
                int(line[4])
            ]
        )
    except KeyError:
        exon_data[parent] = [
            [
                int(line[3]),
                int(line[4])
            ]
        ]


exon_coords = {}
for k in exon_data:
    ranges = exon_data[k]
    all_coords = []
    for start, end in ranges:
        all_coords += [i for i in range(start, end)]
    exon_coords[k] = all_coords

print("Assembling datapoints")
should_be_together = {}
for dp in datapoints:
    dp_coords = [int(i) for i in dp["coordinates"]]
    for k in exon_coords:
        coords = exon_coords[k]
        if all(i in coords for i in dp_coords):
            f = open(f"{dest_dir}/{k}_dps_to_assemble.txt", "a")
            line = f"{dp['name']} - {dp['coordinates']}\n"
            f.write(line)


