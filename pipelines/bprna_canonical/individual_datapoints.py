
base_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions"
fpath = f"{base_dir}/bprna_matched_set_0.txt"

with open(fpath) as fh:
    data = [line.split(", ") for line in fh.readlines()]

datapoint = set()

for d in data:
    dp = d[1]
    seq = d[3]
    stc = d[4]
    line = f"{dp}, {seq}, {stc}"
    datapoint.add(line)


# Should be 61,284
target = 61284
print(f"Writing {len(datapoint)} datapoints (should be {target})")
with open(f"{base_dir}/all_bprna_datapoints.txt", "w") as fh:
    for dp in datapoint:
        fh.write(f"{dp}\n")
