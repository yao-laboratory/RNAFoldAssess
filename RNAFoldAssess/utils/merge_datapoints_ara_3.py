import os, json


prefix = "rasp_arabidopsis_"
suffix = ".json"

json_dir = "/common/yesselmanlab/ewhiting/data/rasp_data/processed/arabidopsis/round2"
master_coords_dir = "/common/yesselmanlab/ewhiting/data/rasp_data/ara-tha/coordinate_files"
seq_dir = "/common/yesselmanlab/ewhiting/data/rasp_data/ara-tha/sequences"

chromosome_map = {}

json_files = [f for f in os.listdir(json_dir) if prefix in f and suffix in f]
for jf in json_files:
    chromosome = jf[len(prefix):][:-len(suffix)]
    chromosome_map[chromosome] = {
        "json": f"{json_dir}/{jf}",
        "coords": f"{master_coords_dir}/{chromosome}.coords",
        "seq": f"{seq_dir}/{chromosome}.seq"
    }

# For testing
exon_locs_raw = {}
ch_1_coord_loc = chromosome_map["chromosome_3"]["coords"]
ch_1_seq_loc = chromosome_map["chromosome_3"]["seq"]
ch_1_json_loc = chromosome_map["chromosome_3"]["json"]
with open(ch_1_coord_loc) as cf:
    coord_data = cf.readlines()

with open(ch_1_seq_loc) as sf:
    seq_data = sf.read().strip()

for index in range(0, len(coord_data), 2):
    exon = coord_data[index].strip()
    locs = [i for i in coord_data[index+1].strip().split(",")]
    exon_locs_raw[exon] = locs

with open(ch_1_json_loc) as jf:
    datapoints = json.load(jf)

# exon_seqs_raw = {}
# for exon, locs in exon_locs_raw.items():
#     if len(locs) < 1:
#         continue
#     locs = [int(i) for i in locs if i != ""]
#     seq = "".join([seq_data[i] for i in locs])
#     exon_seqs_raw[exon] = seq

f = open(f"/common/yesselmanlab/ewhiting/data/rasp_data/loc_info_chromosome_3.txt", "w") # new

# exon_dp_map = {}
counter = 0
len_data = len(exon_locs_raw)
for exon, locs in exon_locs_raw.items():
    counter += 1
    if counter % 250 == 0:
        print(f"Working #{counter} of {len_data}, {exon}")
    f.write(f"{exon}\n") # new
    for dp in datapoints:
        if all(i in locs for i in dp["coordinates"]):
            f.write(f"{dp.name}\n") # new
            # try:
            #     exon_dp_map[exon].append(dp)
            # except KeyError:
            #     exon_dp_map[exon] = [dp]
            # break



print("Done")
