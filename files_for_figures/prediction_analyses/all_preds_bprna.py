import os, shutil


import pandas as pd


bprna_loc = "/work/yesselmanlab/ewhiting/bprna_preds/redo_reports"

def get_file_loc(model):
    return f"{bprna_loc}/{model}_master_1_lenience.txt"

models = [
    "ContextFold",
    "ContraFold",
    "EternaFold",
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

all_pred_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions"
all_pred_file = open(f"{all_pred_dir}/bprna_master_file.txt", "w")
headers = "dataset, model, dp_name, sequence, true_structure, predicted_structure, sensitivity, ppv, f1\n"
all_pred_file.write(headers)

for m in models:
    pred_path = get_file_loc(m)
    with open(pred_path) as fh:
        data = fh.readlines()

    if data[0].startswith("model_name") or data[0].startswith("algo_name"):
        data.pop(0)

    for d in data:
        d = d.split(", ")
        dp_name = d[1]
        # Temp workaround
        # if dp_name in ["bpRNA_SPR_316", "bpRNA_SPR_184"]:
        #     continue
        seq = d[3]
        if "_" in seq or "." in seq:
            continue
        true_structure = d[4]
        pred = d[5]
        s = d[6]
        p = d[7]
        f = d[8].strip()
        for metric in [s, p, f]:
            try:
                float(metric)
            except ValueError as e:
                raise Exception(f"Couldn't turn {metric} to float in {dp_name} in {m}: {e}")

        line = f"bpRNA, {m}, {dp_name}, {seq}, {true_structure}, {pred}, {s}, {p}, {f}\n"
        all_pred_file.write(line)


all_pred_file.close()
