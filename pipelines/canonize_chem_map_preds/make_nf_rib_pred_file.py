import os

from RNAFoldAssess.models import CanonicalBasePairScorer, DataPoint
from RNAFoldAssess.models.scorers import *


dbn_dir = "/work/yesselmanlab/ewhiting/outputs/ribonanza"
files = os.listdir(dbn_dir)

dest_dir = f"/mnt/nrdstor/yesselmanlab/ewhiting/reports/ribonanza/canonical"

ribo_data_csv = "/mnt/nrdstor/yesselmanlab/ewhiting/rna_data/ribonanza/rmdb_data.v1.3.0.csv"
with open(ribo_data_csv) as fh:
    data = fh.readlines()

data.pop(0)
data = [d.split(",") for d in data]

experiment_map = {
    "BzCN_cotx": "DMS4",
    "DMS_M2_seq": "DMS4",
    "DMS_cotx": "DMS4",
    "DMS": "DMS4",
    "1M7": "SHAPE",
    "NMIA": "SHAPE",
    "BzCN": "SHAPE",
    "deg_Mg_50C": "SHAPE",
    "deg_50C": "SHAPE",
    "deg_pH10": "SHAPE",
    "deg_Mg_pH10": "SHAPE",
    "CMCT": "CMCT"
}

r1_index = 7
dp_map = {}
for d in data:
    name = d[0]
    seq = d[1]
    experiment_type = d[2]
    chemical_mapping_method = experiment_map[experiment_type]
    reactivities = d[r1_index:len(seq) + r1_index]
    dp_map[name] = {
        "sequence": seq,
        "reactivities": reactivities,
        "method": chemical_mapping_method
    }



fstring = ""


for f in files:
    dp_name = f.split(".")[0]
    with open(f"{dbn_dir}/{f}") as fh:
        dbn_data = fh.readlines()

    orig_pred = dbn_data[3].strip()
    dp = dp_map[dp_name]
    seq = dp["sequence"]
    new_pred = CanonicalBasePairScorer.transform_structure(orig_pred, seq)
    reactivities = dp["reactivities"]
    testable_seq = ""
    testable_dbn = ""
    testable_reactivities = []
    for i, reactivity in enumerate(reactivities):
        if reactivity != "":
            testable_seq += seq[i]
            testable_dbn += new_pred[i]
            testable_reactivities.append(float(reactivity))

    chemical_mapping_method = dp_map[dp_name]["method"]

    if chemical_mapping_method in ["DMS4", "SHAPE"]:
        score = DSCI.score(
            testable_seq,
            testable_dbn,
            testable_reactivities,
            SHAPE=True
        )
    else:
        score = DSCI.score(
            testable_seq,
            testable_dbn,
            testable_reactivities,
            CMCT=True
        )

    acc = score["accuracy"]
    p = score["p"]

    new_line = f"NeuralFold, {dp_name}, {seq}, {new_pred}, {acc}, {p}\n"
    fstring += new_line


with open(f"{dest_dir}/NeuralFold_all_predictions.txt", "w") as fh:
    fh.write(fstring)
