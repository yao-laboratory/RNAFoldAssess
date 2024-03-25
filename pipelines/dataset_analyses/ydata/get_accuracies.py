import os
import pandas as pd


base_dir = "/common/yesselmanlab/ewhiting/reports/ydata"

def file_name(model_name):
    return f"{base_dir}/{model_name}_YesselmanDMS_report.txt"


accuracies = []
models = [
    "ContextFold",
    "ContraFold",
    "EternaFold",
    "IPknot",
    "MXFold",
    "RandomPredictor",
    "RNAFold",
    "SeqFold"
]

for m in models:
    path = file_name(m)
    f = open(path)
    data = f.readlines()
    f.close()
    # Get rid of headers
    if data == []:
        continue
    data.pop(0)
    for d in data:
        acc = float(d.split(", ")[4])
        accuracies.append(acc)


s = pd.Series(accuracies)
descriptive_stats = s.describe()
f = open("YDataAccuracies.txt", "w")
f.write(str(descriptive_stats))
f.close()
