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
    # "SPOT-RNA"
]

all_pred_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions"
all_pred_file = open(f"{all_pred_dir}/bprna_master_file.txt", "w")

# TODO
