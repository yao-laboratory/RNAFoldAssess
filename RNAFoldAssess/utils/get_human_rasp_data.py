import os


print("Opening gff file")
base_dir = "/common/yesselmanlab/ewhiting/data/rasp_data/human"
with open(f"{base_dir}/hg38.gff3") as f:
    gff_data = [d.split("\t") for d in f.readlines()]

print("Finished reading gff file")
print("Filtering data")
gff_data = [d for d in gff_data if d[2].lower() == "exon"]
print("Done filtering")
len_data = len(gff_data)
print(f"Loaded {len_data} lines into `gff_data` variable")

print("Getting locations")
locs = []
for d in gff_data:
    start = int(d[3])
    finish = int(d[4])
    sign = d[6]
    locs.append(
        (start, finish, sign)
    )

print(f"Loaded {len(locs)} location data into `locs` variable")

bed_file_loc = f"{base_dir}/DMS-MaPseq_hg38_Nature_Methods_2017_DMS_invivo_score_both_score_DMSMapSeq_2017.score.bed"

print("Loading bed file")
with open(bed_file_loc) as f:
    bed_data = f.readlines()
print("Finished loading bed file")
print(f"Loaded {len(bed_data)} lines into `bed_data` variable")

breakpoint()

