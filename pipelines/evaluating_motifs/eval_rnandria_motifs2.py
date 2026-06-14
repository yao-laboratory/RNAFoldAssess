import json


base_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/rnandria/motifs"

with open(f"{base_dir}/rnandria_pos_map.json") as fh:
    data = json.load(fh)

# Example: hsa-mir-7702

for dp in data:
    positions = data[dp]["positions"]
