import os

from RNAFoldAssess.models import CanonicalBasePairScorer, DataPoint
from RNAFoldAssess.models.scorers import *


ribo_data_csv = "/mnt/nrdstor/yesselmanlab/ewhiting/rna_data/ribonanza/rmdb_data.v1.3.0.csv"
with open(ribo_data_csv) as fh:
    data = fh.readlines()

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


pred_path = "/work/yesselmanlab/ewhiting/outputs/ribonanza/"
dbn_files = os.listdir(pred_path)

fstring = ""
for df in dbn_files:
    dp_name = df.split(".")[0]

    with open(f"{pred_path}/{df}") as fh:
        dbn_data = fh.readlines()

    dp = dp_map[dp_name]
    prediction = dbn_data[3].strip()
    prediction = CanonicalBasePairScorer.transform_structure(dbn, dp["sequence"])
    testable_seq = ""
    testable_dbn = ""
    testable_reactivities = []
    for i, reactivity in enumerate(dp["reactivities"]):
        if reactivity != "":
            testable_seq += dp["sequence"][i]
            testable_dbn += prediction[i]
            testable_reactivities.append(float(reactivity))

    chem_map_method = dp["method"]

    if chem_map_method in ["DMS4", "SHAPE"]:
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

    seq = dp["sequence"]
    new_line = f"NeuralFold, {dp_name}, {seq}, {prediction}, {acc}, {p}\n"
    fstring += new_line


with open(f"{dest_dir}/NeuralFold_canonical_predictions.txt", "w") as fh:
    fh.write(fstring)

print("Done")
