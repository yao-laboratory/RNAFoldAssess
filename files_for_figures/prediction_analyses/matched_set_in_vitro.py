import os


all_pred_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions"
with open(f"{all_pred_dir}/chemical_mapping_master_file.txt") as pf:
    data = pf.readlines()

datapoints = {}
model_map = {}

print("Reading data ...")
for d in data:
    datapoint = d.split(", ")[1]
    model = d.split(", ")[0]
    try:
        datapoints[datapoint] += 1
    except KeyError:
        datapoints[datapoint] = 1
    try:
        model_map[model] += 1
    except KeyError:
        model_map[model] = 1

for m, vals in model_map.items():
    print(f"{m}: {vals}")

for dp, c in datapoints.items():
    if c > 14:
        print(dp)

all_counts = list(datapoints.values())
print(f"Max count: {max(all_counts)}")
print(f"Min count: {min(all_counts)}")
print(f"Avg count: {sum(all_counts) / len(all_counts)}")

print("Writing data")
matched_set_file = open(f"{all_pred_dir}/chemical_mapping_matched_set.txt", "w")
counter = 0
for d in data:
    counter += 1
    if counter % 150000 == 0:
        print(f"Working {counter} of {len(data)}")
    dp = d.split(", ")[1]
    count = datapoints[dp]
    if count == 14:
        matched_set_file.write(d)

matched_set_file.close()
