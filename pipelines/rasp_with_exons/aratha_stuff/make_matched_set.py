import os


models = [
    "ContextFold",
    "ContraFold",
    "EternaFold",
    "IPKnot",
    "NeuralFold",
    "NUPACK",
    "RNAFold",
    "RNAStructure",
    "pKnots",
    "Simfold",
    "MXFold",
    "MXFold2",
    "SPOT-RNA"
]

master_file_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions"
with open(f"{master_file_dir}/all_rasp_arabidopsis_preds.txt") as fh:
    lines = fh.readlines()

datapoints = set()
for line in lines:
    line = line.split(", ")
    dp = line[1]
    datapoints.add(dp)

dp_model_map = {}
for dp in datapoints:
    dp_model_map[dp] = {}

for line in lines:
    line = line.split(", ")
    model = line[0]
    dp = line[1]
    acc = line[4]

    dp_model_map[dp][model] = acc

matched_dps = []
for dp in dp_model_map:
    model_preds = len(dp_model_map[dp])
    if model_preds >= len(models):
        matched_dps.append(dp)

most_model_counts = {}
for m in models:
    most_model_counts[m] = 0

print(f"There are {len(dp_model_map)} datapoints")
for dp, models in dp_model_map.items():
    for m in models:
        most_model_counts[m] += 1

for m in most_model_counts:
    print(f"{m} predicted {most_model_counts[m]} datapoints")

print()


matched_lines = []
for line in lines:
    dp = line.split(", ")[1]
    if dp in matched_dps:
        matched_lines.append(line)

with open(f"{master_file_dir}/rasp_ara_matched_set.txt", "w") as fh:
    fh.write("".join(matched_lines))


