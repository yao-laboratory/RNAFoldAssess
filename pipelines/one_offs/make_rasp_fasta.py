import os, json


species = "ara-tha"
base_dir = "/common/yesselmanlab/ewhiting/data/rasp_data"
json_dir = f"{base_dir}/{species}/json_files"
json_files = os.listdir(json_dir)
ch_map = {}
for jf in json_files:
    ch = jf.replace("_exons.json", "")
    with open(f"{json_dir}/{jf}") as fh:
        ch_map[ch] = json.load(fh)


fasta_dir = f"{base_dir}/fasta_files_gt_10/{species}"

for ch, exon_data in ch_map.items():
    print(f"Working {ch} datapoints")
    ch_fasta_dir = f"{fasta_dir}/{ch}"
    # Make the directory if it doesn't exist
    if not os.path.exists(ch_fasta_dir):
        os.mkdir(ch_fasta_dir)

    for data in exon_data:
        name = data["name"]
        seq = data["sequence"]
        fasta_string = f">{name}\n{seq}"
        with open(f"{ch_fasta_dir}/{name}.fasta", "w") as fh:
            fh.write(fasta_string)
