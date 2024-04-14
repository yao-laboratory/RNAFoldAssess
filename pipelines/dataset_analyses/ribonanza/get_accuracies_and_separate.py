import os
import pandas as pd


base_dir = "/common/yesselmanlab/ewhiting/reports/ribonanza/with_energies"

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

hi_bound = descriptive_stats["75%"]
low_bound = descriptive_stats["25%"]

destination_dir = "/common/yesselmanlab/ewhiting/dataset_analyses/ribonanza"
lo_preds_file = open(f"{destination_dir}/Ribo_lo_accuracy_predictions.txt", "w")
mid_preds_file = open(f"{destination_dir}/Ribo_mid_accuracy_predictions.txt", "w")
hi_preds_file = open(f"{destination_dir}/Ribo_hi_accuracy_predictions.txt", "w")

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
            items = d.split(", ")
            data_point = items[1]
            acc = float(items[4])
            if acc <= low_bound:
                lo_preds_file.write(d)
            elif acc >= hi_bound:
                hi_preds_file.write(d)
            else:
                mid_preds_file.write(d)


lo_preds_file.close()
mid_preds_file.close()
hi_preds_file.close()

