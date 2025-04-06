base_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions"


ref_file = f"{base_dir}/pdb_canonical_matched_1.txt"
with open(ref_file) as fh:
    data = [line.split(", ") for line in fh.readlines()]

dp_data_map = {}

for d in data:
    dp = d[1]
    if dp not in dp_data_map:
        seq = d[2]
        stc = d[3]
        dp_data_map[dp] = {"seq": seq, "stc": stc}


if len(dp_data_map) != 264:
    raise Exception(f"Something wrong. Found {len(dp_data_map)} datapoints, should have found 264")


report = ""
for d, vals in dp_data_map.items():
    line = f"{d}, {vals['seq']}, {vals['stc']}\n"
    report += line

with open(f"{base_dir}/all_pdb_datapoints.txt", "w") as fh:
    fh.write(report)
