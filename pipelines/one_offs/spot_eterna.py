import os

from RNAFoldAssess.models import DataPoint, EternaDataPoint
from RNAFoldAssess.models.scorers import *


data_points_path = "/common/yesselmanlab/ewhiting/data/translated_eterna_data/eterna.json"
dbn_path = "/work/yesselmanlab/ewhiting/spot_outputs/eterna_dbn_files"
report_path = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/eterna_data"

datapoints = EternaDataPoint.factory(data_points_path)
shape_datapoints = []
dms_datapoints = []
all_accs = []

fail_count = 0
for dp in datapoints:
    if dp.mapping_method == "SHAPE":
        shape_datapoints.append(dp)
    elif dp.mapping_method == "DMS":
        dms_datapoints.append(dp)


fname = "SPOT-RNA_SHAPE_pipeline_report.txt"
shape_rf = open(f"{report_path}/{fname}", "w")
for dp in shape_datapoints:
    dbn_file = f"{dbn_path}/{dp.name}.ct.dbn"
    if not os.path.exists(dbn_file):
        continue
    with open(dbn_file) as f:
        dbn_data = f.readlines()
    try:
        pred = dbn_data[2].strip()
        score = dp.assess_prediction(pred)
        acc = score["accuracy"]
        p = score["p"]
        all_accs.append(acc)
        line = f"SPOT-RNA, {dp.name}, {dp.sequence}, {pred}, {acc}, {p}\n"
        shape_rf.write(line)
    except:
        continue

shape_rf.close()

fname = "SPOT-RNA_DMS_pipeline_report.txt"
dms_rf = open(f"{report_path}/{fname}", "w")
for dp in dms_datapoints:
    dbn_file = f"{dbn_path}/{dp.name}.ct.dbn"
    if not os.path.exists(dbn_file):
        continue
    with open(dbn_file) as f:
        dbn_data = f.readlines()
    try:
        pred = dbn_data[2].strip()
        score = dp.assess_prediction(pred)
        acc = score["accuracy"]
        p = score["p"]
        all_accs.append(acc)
        line = f"SPOT-RNA, {dp.name}, {dp.sequence}, {pred}, {acc}, {p}\n"
        dms_rf.write(line)
    except:
        continue

dms_rf.close()

print(f"Collected {len(all_accs)} datapoints")
print(sum(all_accs) / len(all_accs))
