import os

base_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions"
master_file = f"{base_dir}/rasp_microbe_master_predictions.txt"

with open(master_file) as fh:
    lines = [d.split(", ") for d in fh.readlines()]


model_index = 0
dp_index = 1
acc_index = 4

models = [
    "ContextFold",
    "ContraFold",
    "EternaFold",
    "IPKnot",
    "MXFold",
    "MXFold2",
    "NeuralFold",
    "NUPACK",
    "pKnots",
    "RNAFold",
    "RNAStructure",
    "Simfold",
    "SPOT-RNA"
]

total_models = len(models)

print("Building dp map")
all_dps = set()
for line in lines:
    dp = line[dp_index]
    all_dps.add(dp)

dp_map = {}
for dp in all_dps:
    dp_map[dp] = []


for line in lines:
    dp = line[dp_index]
    m = line[model_index]
    dp_map[dp].append(m)

matched_dps = set()
for dp in dp_map:
    dp_count = len(dp_map[dp])
    if dp_count > total_models:
        print(f"More than {total_models} predictions for {dp}")
    elif dp_count == total_models:
        matched_dps.add(dp)


matched_dps = list(matched_dps)
matched_lines = []
for line in lines:
    dp = line[dp_index]
    if dp in matched_dps:
        matched_lines.append(", ".join(line))


with open(f"{base_dir}/rasp_microbe_matched_set.txt", "w") as fh:
    fh.write("".join(matched_lines))
