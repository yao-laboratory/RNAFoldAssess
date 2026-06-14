import os, json

from RNAFoldAssess.models import DataPoint
from RNAFoldAssess.models.scorers import *


species = "ara-tha"
existing_report_dir = f"/mnt/nrdstor/yesselmanlab/ewhiting/reports/rasp_data/{species}"
dest_dir = f"{existing_report_dir}/canonical"

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

base_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/data/rasp_data"
json_dir = f"{base_dir}/{species}/json_files"
json_files = os.listdir(json_dir)

all_data = []
for jf in json_files:
    with open(f"{json_dir}/{jf}") as fh:
        all_data += json.load(fh)

print("Making datapoint map")
dp_map = {}
for d in all_data:
    dp_map[d['name']] = d
print("Done making datapoint map")

for m in models:
    print(f"Working {m}")
    files = [f for f in os.listdir(existing_report_dir) if f"{m}_" in f]
    lines = []
    for f in files:
        with open(f"{existing_report_dir}/{f}") as fh:
            preds = fh.readlines()
            if preds[0].startswith("algo"):
                preds.pop(0)
        lines += preds

    lines = [line.split(", ") for line in lines]
    fstring = ""
    for line in lines:
        dp_name = line[1]
        dp = dp_map[dp_name]
        seq = dp["sequence"]
        orig_pred = line[3]
        new_pred = CanonicalBasePairScorer.transform_structure(orig_pred, seq)
        reactivity_map = dp["reactivity_map"]
        reactivities = [float(d[1]) for d in reactivity_map]

        testable_seq = ""
        testable_dbn = ""
        for i, _reactivity in reactivity_map:
            testable_seq += seq[i]
            testable_dbn += new_pred[i]

        chem_map_method = dp["chem_map_type"]

        if chem_map_method == "DMS":
            score = DSCI.score(
                testable_seq,
                testable_dbn,
                reactivities,
                DMS=True
            )
        elif chem_map_method == "SHAPE":
            score = DSCI.score(
                testable_seq,
                testable_dbn,
                reactivities,
                SHAPE=True
            )

        acc = score["accuracy"]
        p = score["p"]
        fline = f"{m}, {dp_name}, {seq}, {new_pred}, {acc}, {p}\n"
        fstring += fline

    with open(f"{dest_dir}/{m}_{species}_predictions.txt", "w") as fh:
        fh.write(fstring)

print("Done")
