import os


all_pred_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions"
with open(f"{all_pred_dir}/chemical_mapping_master_file.txt") as pf:
    data = pf.readlines()

datapoints = {}
model_map = {}

print("Reading data ...")
for d in data:
    # datapoint = d.split(", ")[1]
    model = d.split(", ")[1]
    try:
        model_map[model] += 1
    except KeyError:
        model_map[model] = 1


max_val = max(list(model_map.values()))

for m, vals in model_map.items():
    print(f"{m}: {vals}, {round(vals / max_val, 4) * 100}%")
    print(f"\tMissing {max_val - vals} datapoints")


