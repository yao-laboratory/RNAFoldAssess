import json

# With YData:
# n = 3,337,858
# q1 = 0.7546113306982872
# q2 = 0.8961038961038961
# q3 = 0.9605263157894737
#
# Without YData:
# n = 1,407,263
# q1 = 0.6367672305654741
# q2 = 0.7543103448275862
# q3 = 0.8687169312169312

base_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions"
json_file_path = f"{base_dir}/chem_map_preds_and_scores.json"

with open(json_file_path) as fh:
    data = json.load(fh)

q1 = 0.6368
q3 = 0.8687

dp_map = {}

print("Counting scores")
for dp in data.keys():
    dp_map[dp] = {
        "low": 0,
        "high": 0
    }


for dp, dp_data in data.items():
    if dp_data["dataset"] == "YData":
        continue
    preds = dp_data["preds"]
    for m in preds:
        if "score" not in preds[m]:
            continue
        score = preds[m]["score"]
        if score <= q1:
            dp_map[dp]["low"] += 1
        if score >= q3:
            dp_map[dp]["high"] += 1


print("Spot checking predictions")
for dp in dp_map:
    if dp_map[dp]["low"] > 13:
        print(f"Anomaly in {dp}")
    if dp_map[dp]["high"] > 13:
        print(f"Anomaly in {dp}")

print("Writing files")
easy_dp_file = open(f"{base_dir}/easy_chem_map_datapoints.txt", "w")
hard_dp_file = open(f"{base_dir}/hard_chem_map_datapoints.txt", "w")

for dp in dp_map:
    if dp_map[dp]["low"] >= 13:
        hard_dp_file.write(f"{dp}\n")
    elif dp_map[dp]["high"] >= 13:
        easy_dp_file.write(f"{dp}\n")

for f in [easy_dp_file, hard_dp_file]:
    f.close()


