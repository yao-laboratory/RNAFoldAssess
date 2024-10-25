import os


all_pred_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions"
with open(f"{all_pred_dir}/chemical_mapping_master_file.txt") as pf:
    data = pf.readlines()

datapoints = {}
model_map = {}
models = set()

print("Reading data ...")
for d in data:
    line = d.split(", ")
    model = line[1]
    dp = line[2]
    models.add(model)
    try:
        datapoints[dp].append(model)
    except KeyError:
        datapoints[dp] = [model]


for m in models:
    model_map[m] = []

print(f"There are {len(models)} total models")
print(f"There are {len(datapoints)} total datapoints")

dps_with_missing_models = []
for dp, models in datapoints.items():
    if len(models) < 14:
        dps_with_missing_models.append(dp)

print(f"There are {len(dps_with_missing_models)} datapoints that are missing models")
total_missing = 0

for mm in model_map:
    print(f"Working {mm}")
    for dp, models in datapoints.items():
        if mm not in models:
            model_map[mm].append(dp)
    missing_dps = len(model_map[mm])
    total_missing += missing_dps
    print(f"\t{mm} is missing {missing_dps} datapoints")
    with open(f"{mm}_missing_dps.txt", "w") as fh:
        for dp in model_map[mm]:
            fh.write(f"{dp}\n")

print(f"In total there are {total_missing} missing datapoint predictions")
