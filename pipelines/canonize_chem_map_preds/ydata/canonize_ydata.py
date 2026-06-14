import os

from RNAFoldAssess.models import DataPoint
from RNAFoldAssess.models.scorers import *


base_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/ydata"
existing_pred_dir = f"{base_dir}/remove_dups"
dest_dir = f"{base_dir}/canonize"

dp_file_path = "/mnt/nrdstor/yesselmanlab/ewhiting/ss_deeplearning_data/data"

approved_cohorts = [
    "C014G",
    "C014H",
    "C014I",
    "C014J",
    "C014U",
    "C014V"
]

datapoints = []

data_point_files = os.listdir(dp_file_path)
for dpf in os.listdir(dp_file_path):
    cohort = dpf.split(".")[0]
    if cohort not in approved_cohorts:
        continue

    datapoints += DataPoint.factory(f"{dp_file_path}/{dpf}", cohort)


print("Making dp map")
dp_map = {}
for dp in datapoints:
    dp_map[dp.name] = dp

print("Done making dp map")

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

for m in models:
    print(f"Working {m}")
    with open(f"{existing_pred_dir}/{m}_YesselmanDMS_report.txt") as fh:
        preds = fh.readlines()

    if preds[0].startswith("algo"):
        preds.pop(0)

    preds = [p.split(", ") for p in preds]

    fstring = ""
    for p in preds:
        dp_name = p[1]
        if dp_name == "datapoint_name":
            # How did this happen?
            continue
        dp = dp_map[dp_name]
        original_pred = p[3]
        new_pred = CanonicalBasePairScorer.transform_structure(original_pred, dp.sequence)

        score = DSCI.score(
            dp.sequence,
            new_pred,
            dp.reactivities,
            DMS=True
        )
        acc = score["accuracy"]
        p = score["p"]

        line = f"{m}, {dp_name}, {dp.sequence}, {new_pred}, {acc}, {p}\n"
        fstring += line

    with open(f"{dest_dir}/{m}_YesselmanDMS_report.txt", "w") as fh:
        fh.write(fstring)

print("Done")
