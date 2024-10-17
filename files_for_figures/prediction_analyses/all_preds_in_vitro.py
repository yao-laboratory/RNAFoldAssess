import os, shutil


import pandas as pd


datasets = {
    "EternaData": "/mnt/nrdstor/yesselmanlab/ewhiting/reports/eterna_data/with_energy",
    "Ribonanza": "/mnt/nrdstor/yesselmanlab/ewhiting/reports/ribonanza/unique_preds",
    "RNAndria": "/mnt/nrdstor/yesselmanlab/ewhiting/reports/rnandria",
    "YesselmanLab": "/mnt/nrdstor/yesselmanlab/ewhiting/reports/ydata"
}
ds_len = len(datasets)

models = [
    "ContextFold",
    "ContraFold",
    "EternaFold",
    "RandomPredictor",
    "IPKnot",
    "NeuralFold",
    "NUPACK",
    "RNAFold",
    "RNAStructure",
    "pKnots",
    "Simfold",
    "MXFold",
    "MXFold2",
    "SPOT-RNA"
]

len_models = len(models)

all_pred_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions"
all_pred_file = open(f"{all_pred_dir}/chemical_mapping_master_file.txt", "w")

for m in models:
    print(f"Working {m} predictions")
    for i, ds in enumerate(datasets):
        print(f"\tWorking {ds} - {i} of {ds_len}")
        loc = datasets[ds]
        all_preds = [f for f in os.listdir(loc) if f"{m}_" in f] # Underscore to prevent double counting MXFold
        # Filter to just the prediction files
        if ds == "YesselmanLab":
            all_preds = [f for f in all_preds if "report" in f]
        elif ds in ["Ribonanza", "RNAndria"]:
            all_preds = [f for f in all_preds if "predictions" in f]

        print(f"\tOpening files for {ds}")
        for pred_file in all_preds:
            pf = open(f"{loc}/{pred_file}")
            data = pf.readlines()
            pf.close()

            if len(data) == 0:
                print(f"No data in {pred_file}")
                continue
            # Pop headers if necessary
            if data[0].startswith("algo"):
                data.pop(0)

            data = [d.split(", ") for d in data]

            dp_loc = 1
            seq_loc = 2
            pred_loc = 3
            acc_loc = 4

            for d in data:
                try:
                    name = d[dp_loc]
                    seq = d[seq_loc]
                    pred = d[pred_loc]
                    acc = d[acc_loc]

                    if ds == "YesselmanLab":
                        cohort = name.split("_")[0]
                        if cohort not in ["C014G", "C014H", "C014I", "C014J", "C014U", "C014V"]:
                            continue

                    line = f"{m}, {name}, {seq}, {pred}, {acc}\n"
                    all_pred_file.write(line)
                except IndexError:
                    print(f"Index error in {m}, {ds}, {pred_file}, {d}")
                    continue

all_pred_file.close()
