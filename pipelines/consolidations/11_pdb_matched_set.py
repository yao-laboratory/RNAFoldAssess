base_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/consolidated"
loc = f"{base_dir}/pdb_all_preds_1_lenience.txt"

with open(loc) as fh:
    lines = fh.readlines()

lines.pop(0)
lines = [line.split(", ") for line in lines]

datapoints = set()
# models = set()
for line in lines:
    datapoints.add(line[1])

dp_map = {}
for dp in datapoints:
    dp_map[dp] = []

for line in lines:
    dp = line[1]
    model = line[0]
    dp_map[dp].append(model)

matched_dps = set()
for dp, models in dp_map.items():
    if len(models) == 13:
        matched_dps.add(dp)


good_lines = []

for line in lines:
    dp = line[1]
    if dp in matched_dps:
        good_lines.append(", ".join(line))

with open(f"{base_dir}/pdb_matched_set_1.txt", "w") as fh:
    fh.write("".join(good_lines))
