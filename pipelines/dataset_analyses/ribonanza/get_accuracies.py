import os
import pandas as pd


base_dir = "/common/yesselmanlab/ewhiting/reports/ribonanza"

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

chem_mapping_types = [
    "1M7",
    "BzCN_cotx",
    "BzCN",
    "CMCT",
    "deg_50C",
    "deg_Mg_50C",
    "deg_Mg_pH10",
    "deg_pH10",
    "DMS_cotx",
    "DMS_M2_seq",
    "DMS",
    "NMIA"
]

for m in models:
    print(f"Working {m}")
    for cmt in chem_mapping_types:
        print(f"\t- {cmt}")
        file_path = f"{m}_{cmt}_predictions.txt"
        f = open(f"{base_dir}/{file_path}")
        data = f.readlines()
        f.close()
        if data == []:
            continue
        for d in data:
            d = d.split(", ")
            acc = float(d[4])
            accuracies.append(acc)


s = pd.Series(accuracies)
descriptive_stats = s.describe()
f = open("RibonanzaDataAccuracies.txt", "w")
f.write(str(descriptive_stats))
f.close()
