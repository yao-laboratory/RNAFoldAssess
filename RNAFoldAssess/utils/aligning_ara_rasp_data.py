import json, os


gff_loc = "/common/yesselmanlab/ewhiting/data/rasp_data/ara-tha/TAIR10.gff3"
json_dir = "/common/yesselmanlab/ewhiting/data/rasp_data/processed/arabidopsis/round2"
files = os.listdir(json_dir)

datapoints = []

print("Loading datapoints from JSON files")
for f in files:
    with open(f"{json_dir}/{f}") as ff:
        datapoints += json.load(ff)

# coordinate key: coordinates
all_coords = []
print("Setting coordinate index variable")
for dp in datapoints:
    all_coords += dp["coordinates"]

print(f"There are {len(all_coords)} coordinates from the bed file")


print("Reading genome file")

with open(gff_loc) as gf:
    gff_data = [d.split("\t") for d in gf.readlines()]

exon_coords = []
for gd in gff_data:
    desc = gd[2]
    if desc == "exon":
        start = int(gd[3])
        end = int(gd[4])
        exon_coords.append([start, end])

print(f"There are {len(exon_coords)} exons")

print("Getting exons that can be assembled")
# For testing:
exon_coords = exon_coords[100:1000]
can_be_assembled = []
for coord in exon_coords:
    if coord[1] in all_coords:
        can_be_assembled.append(coord)


print(f"There are {len(can_be_assembled)} sequences able to be assembled")
breakpoint()

should_be_together = []
for coord in can_be_assembled:
    print("AAAAAHHHHHHHH")

