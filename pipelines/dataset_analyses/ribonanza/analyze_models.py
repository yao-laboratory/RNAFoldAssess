import os
import pandas as pd


destination_dir = "/common/yesselmanlab/ewhiting/reports/ribonanza/analyses"


lo_preds_file = open(f"{destination_dir}/Ribo_lo_accuracy_predictions.txt")
mid_preds_file = open(f"{destination_dir}/Ribo_mid_accuracy_predictions.txt")
hi_preds_file = open(f"{destination_dir}/Ribo_hi_accuracy_predictions.txt")


model_scores = {}

models = [
    "ContextFold",
    "ContraFold",
    "EternaFold",
    "IPKnot",
    "MXFold",
    "RandomPredictor",
    "RNAFold",
    "SeqFold"
]

models_count = len(models)

for m in models:
    model_scores[m] = {
        "low": 0,
        "middle": 0,
        "high": 0
    }


lo_data = lo_preds_file.readlines()
lo_preds_file.close()

key = "low"
for d in lo_data:
    items = d.split(", ")
    model_name = items[0]
    model_scores[model_name][key] += 1

mid_data = mid_preds_file.readlines()
mid_preds_file.close()

key = "middle"
for d in mid_data:
    items = d.split(", ")
    model_name = items[0]
    model_scores[model_name][key] += 1

hi_data = hi_preds_file.readlines()
hi_preds_file.close()

key = "high"
for d in hi_data:
    items = d.split(", ")
    model_name = items[0]
    model_scores[model_name][key] += 1


destination = f"{destination_dir}/model_analyses.txt"
f = open(destination, "w")
for m in models:
    score = model_scores[m]
    line = f"{m}\t\t"
    low = score["low"]
    mid = score["middle"]
    hi = score["high"]
    line += f"{low}\t{mid}\t{hi}\n"
    f.write(line)

f.close()
