import json


base_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions"
json_path = f"{base_dir}/motif_prediction_by_datapoint_bprna_trimmed.json"
dp_list_path = f"{base_dir}/bprna_difficult_motifs.txt"

with open(dp_list_path) as fh:
    interesting_datapoints = [line.strip() for line in fh.readlines()]

with open(json_path) as fh:
    json_data = json.load(fh)

datapoints = {}
found_dps = []
# for motif, data in json_data.items():
#     dps = data["found_in_datapoints"]
#     for dp in dps:
#         try:
#             datapoints[dp].append(motif)
#         except KeyError:
#             datapoints[dp] = [motif]

fstring = ""
counter = 0
for motif, data in json_data.items():
    if counter >= 20:
        break
    dps = data["found_in_datapoints"]
    for dp in dps:
        if dp not in found_dps:
            found_dps.append(dp)
            fstring += f"{dp} has a {motif} that is never detected\n"
            counter += 1
            break

with open(f"{base_dir}/small_sample_dp_motifs.txt", "w") as fh:
    fh.write(fstring)
