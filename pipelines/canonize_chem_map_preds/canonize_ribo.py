import os

from RNAFoldAssess.models import CanonicalBasePairScorer, DataPoint
from RNAFoldAssess.models.scorers import *


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
    

existing_pred_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/ribonanza/with_energies"
dest_dir = f"/mnt/nrdstor/yesselmanlab/ewhiting/reports/ribonanza/canonical"

for m in models:
    print(f"Working {m}")
    fstring = ""
    files = [f for f in os.listdir(existing_pred_dir) if f"{m}_" in f and "predictions" in f]
    for f in files:
        with open(f"{existing_pred_dir}/{f}") as fh:
            lines = fh.readlines()
        
        if lines[0].startswith("algo"):
            lines.pop(0)
        
        lines = [line.split(", ") for line in lines]
        for line in lines:
            name = line[1]
            seq = dp_map[name]["sequence"]
            reactivities = dp_map[name]["reactivities"]
            original_pred = line[3]
            new_pred = CanonicalBasePairScorer.transform_structure(original_pred, seq)
            testable_seq = ""
            testable_dbn = ""
            testable_reactivities = []
            for i, reactivity in enumerate(reactivities):
                if reactivity != "":
                    try:
                        testable_seq += seq[i]
                        testable_dbn += new_pred[i]
                        testable_reactivities.append(float(reactivity))
                    except IndexError:
                        breakpoint()
                        print("aww")
                
            sequence = testable_seq
            reactivities = testable_reactivities
            if len(sequence) < 2:
                continue
            
            chemical_mapping_method = dp_map[name]["method"]
            
            if chemical_mapping_method in ["DMS4", "SHAPE"]:
                score = DSCI.score(
                    sequence,
                    testable_dbn,
                    reactivities,
                    SHAPE=True
                )
            else:
                score = DSCI.score(
                    sequence,
                    testable_dbn,
                    reactivities,
                    CMCT=True
                )
            
            acc = score["accuracy"]
            p = score["p"]

            new_line = f"{m}, {name}, {seq}, {new_pred}, {acc}, {p}\n"
            fstring += new_line

    with open(f"{dest_dir}/{m}_canonical_predictions.txt", "w") as fh:
        fh.write(fstring)    

print("Done")
