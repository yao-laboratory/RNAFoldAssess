import os
import pandas as pd


base_dir = "/common/yesselmanlab/ewhiting/reports/rnandria"

def pri_file_name(model_name):
    return f"{base_dir}/{model_name}_rnandria_pri_miRNA_predictions.txt"

def human_file_name(model_name):
    return f"{base_dir}/{model_name}_rnandria_human_mRNA_predictions.txt"

accuracies = []
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

for m in models:
    # Get pri miRNA predictions
    pri_path = pri_file_name(m)
    pf = open(pri_path)
    data = pf.readlines()
    pf.close()
    # Get rid of headers
    if data == []:
        continue
    data.pop(0)
    for d in data:
        d = d.split(", ")
        acc = float(d[4])
        accuracies.append(acc)
    # Get human predictions
    human_path = human_file_name(m)
    hf = open(human_path)
    data = hf.readlines()
    hf.close()
    # Get rid of headers
    if data == []:
        continue
    data.pop(0)
    for d in data:
        d = d.split(", ")
        acc = float(d[4])
        accuracies.append(acc)


s = pd.Series(accuracies)
descriptive_stats = s.describe()
f = open("RNAndriaDataAccuracies.txt", "w")
f.write(str(descriptive_stats))
f.close()
