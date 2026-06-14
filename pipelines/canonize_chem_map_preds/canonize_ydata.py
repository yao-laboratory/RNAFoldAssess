import os, shutil


from RNAFoldAssess.models import CanonicalBasePairScorer, DataPoint
from RNAFoldAssess.models import DSCIException, DSCITypeError, DSCIValueError
from RNAFoldAssess.models.scorers import *


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

# Only have to do SPOT
report_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/ydata/canonize"

# Copy for safe keeping
shutil.copy(f"{report_dir}/SPOT-RNA_YesselmanDMS_report.txt", f"{report_dir}/SPOT-RNA_YesselmanDMS_report.copy.txt")

with open(f'{report_dir}/SPOT-RNA_YesselmanDMS_report.txt') as fh:
    lines = fh.readlines()


lines = [line.split(", ") for line in lines]
fstring = ""
def remove_pseudoknots(stc):
    stc = list(stc)
    for i in range(len(stc)):
        nt = stc[i]
        if nt in "().":
            stc[i] = nt
        elif nt == "<":
            stc[i] = "("
        elif nt == ">":
            stc[i] = ")"
        else:
            stc[i] = "."
    stc = "".join(stc)
    return stc

for line in lines:
    dp_name = line[1]
    dp = dp_map[dp_name]
    prediction = line[3]
    prediction = remove_pseudoknots(prediction)
    prediction = CanonicalBasePairScorer.transform_structure(prediction, dp.sequence)
    score = DSCI.score(
        dp.sequence,
        prediction,
        dp.reactivities,
        DMS=True
    )

    acc = score["accuracy"]
    p = score["p"]

    line = f"SPOT-RNA, {dp_name}, {dp.sequence}, {prediction}, {acc}, {p}\n"
    fstring += line

with open(f'{report_dir}/SPOT-RNA_YesselmanDMS_report.txt', 'w') as fh:
    fh.write(fstring)
