import os
import pandas as pd


base_dir = "/common/yesselmanlab/ewhiting/reports/eterna_data"

def shape_file_name(model_name):
    return f"{base_dir}/{model_name}_SHAPE_pipeline_report.txt"

def dms_file_name(model_name):
    return f"{base_dir}/{model_name}_DMS_pipeline_report.txt"

accuracies = []
models = [
    "ContextFold",
    "ContraFold",
    "EternaFold",
    "IPKnot",
    "MXFold",
    "MXFold2",
    "RandomPredictor",
    "RNAFold",
    "SeqFold"
]

for m in models:
    # Get SHAPE predictions
    shape_path = shape_file_name(m)
    sf = open(shape_path)
    data = sf.readlines()
    sf.close()
    # Get rid of headers
    data.pop(0)
    for d in data:
        d = d.split(", ")
        acc = float(d[4])
        accuracies.append(acc)
    # Get DMS predictions
    dms_path = dms_file_name(m)
    df = open(dms_path)
    data = df.readlines()
    df.close()
    # Get rid of headers
    data.pop(0)
    for d in data:
        d = d.split(", ")
        acc = float(d[4])
        accuracies.append(acc)


s = pd.Series(accuracies)
descriptive_stats = s.describe()
f = open("EternaDataAccuracies.txt", "w")
f.write(str(descriptive_stats))
f.close()
