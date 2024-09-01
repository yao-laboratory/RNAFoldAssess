import json, os, sys

args = sys.argv
given_chromosome = args[1]

acceptable_chromosomes = ["1", "2", "3", "4", "5", "Mt", "Pt"]
if given_chromosome not in acceptable_chromosomes:
    print(f"Unrecognized chromosome for ara-tha: {given_chromosome}. Must be one of {acceptable_chromosomes}")
    sys.exit()

gff_loc = "/common/yesselmanlab/ewhiting/data/rasp_data/ara-tha/TAIR10.gff3"
dest_dir = "/common/yesselmanlab/ewhiting/data/rasp_data/ara-tha/coordinate_files"

print("Reading genome file")

with open(gff_loc) as gf:
    gff_data = [d.split("\t") for d in gf.readlines()]

exon_lines = []
for gd in gff_data:
    if gd[0] == given_chromosome and gd[2] == "exon":
        exon_lines.append(gd)

exon_map = {}

for line in exon_lines:
    chromosome = line[0]
    if chromosome != given_chromosome:
        break
    exon_info = line[8]
    # Example:
    # Parent=transcript:AT1G01010.1;Name=AT1G01010.1.exon1;constitutive=1;ensembl_end_phase=1;ensembl_phase=-1;exon_id=AT1G01010.1.exon1;rank=1
    exon_name = exon_info.split("Name=")[1].split(";")[0]
    try:
        exon_map[exon_name].append([
            int(line[3]),
            int(line[4])
        ])
    except KeyError:
        exon_map[exon_name] = [[
            int(line[3]),
            int(line[4])
        ]]

counter = 0
for exon in exon_map:
    counter += 1
    if counter % 654 == 0:
        print(f"Working exon #{counter}, {exon}")
    file_name = f"{given_chromosome}_{exon}_coords.txt"
    data = exon_map[exon]
    with open(f"{dest_dir}/{file_name}", "a") as cf:
        cf.write(str(data))

print("Done, don't forget to remove duplicates")
