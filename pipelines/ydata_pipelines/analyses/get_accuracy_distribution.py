import os
import pandas as pd


def report_file(model_name):
    return f"/common/yesselmanlab/ewhiting/reports/ydata/{model_name}_YesselmanDMS_report.txt"


model_names = [
    "ContextFold",
    "ContraFold",
    "EternaFold",
    "IPknot",
    "MXFold",
    "RandomPredictor",
    "RNAFold",
    "SeqFold"
]

# Get all accuracies
report_files = []
for m in model_names:
    report_files.append(
        report_file(m)
    )


accuracies = []
for f in report_files:
    file = open(f)
    data = file.readlines()
    file.close()
    # Get rid of header
    data.pop(0)
    for d in data:
        d = d.split(", ")
        accuracies.append(float(d[4]))

s = pd.Series(accuracies)
descriptive_stats = s.describe()
print(descriptive_stats)
