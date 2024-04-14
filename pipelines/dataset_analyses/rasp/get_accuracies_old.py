import os
import pandas as pd


base_dir = "/common/yesselmanlab/ewhiting/reports/rasp_data"

def get_prediction_files(model_name, species):
    predictions_dir = f"{base_dir}/{species}/{model_name}"
    all_files = os.listdir(predictions_dir)
    files = [f"{predictions_dir}/{f}" for f in all_files if f.endswith("predictions.txt")]
    return files

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

rasp_folders = [
    "arabidopsis",
    "covid",
    "ecoli",
    "HIV",
    "human"
]

for folder in rasp_folders:
    for m in models:
        files = get_prediction_files(m, folder)
        for f in files:
            file = open(f)
            data = file.readlines()
            file.close()
            # Get rid of header
            data.pop(0)
            for d in data:
                acc = float(d.split(", ")[4])
                accuracies.append(acc)



s = pd.Series(accuracies)
descriptive_stats = s.describe()
f = open("RASPDataAccuracies.txt", "w")
f.write(str(descriptive_stats))
f.close()
