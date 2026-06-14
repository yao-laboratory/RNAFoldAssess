import json
import numpy as np


base_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions"
json_file_path = f"{base_dir}/chem_map_preds_and_scores.json"

with open(json_file_path) as fh:
    data = json.load(fh)

models = ["ContextFold", "ContraFold", "EternaFold", "IPKnot",
          "NeuralFold", "NUPACK", "RNAFold",
          "RNAStructure", "pKnots", "Simfold",
          "MXFold", "MXFold2", "SPOT-RNA"]

all_accs = []
non_ydata_accs = []

print("Getting scores")

for datapoint, dp_data in data.items():
    dataset = dp_data["dataset"]
    for m in models:
        try:
            acc = dp_data["preds"][m]["score"]
            all_accs.append(acc)
            if dataset != "YData":
                non_ydata_accs.append(acc)
        except KeyError:
            print(f"{m} - {dataset} - {datapoint}")
            continue


print("Getting accuracies")

n = len(all_accs)
q1 = np.percentile(all_accs, 25)
q2 = np.percentile(all_accs, 50)  # This is the median
q3 = np.percentile(all_accs, 75)
report_string = f"n = {n}\nq1 = {q1}\nq2 = {q2}\nq3 = {q3}"

with open(f"{base_dir}/chem_map_quartile_scores.txt", "w") as fh:
    fh.write(report_string)


n = len(non_ydata_accs)
q1 = np.percentile(non_ydata_accs, 25)
q2 = np.percentile(non_ydata_accs, 50)  # This is the median
q3 = np.percentile(non_ydata_accs, 75)
report_string = f"n = {n}\nq1 = {q1}\nq2 = {q2}\nq3 = {q3}"

with open(f"{base_dir}/chem_map_quartile_scores_no_ydata.txt", "w") as fh:
    fh.write(report_string)

