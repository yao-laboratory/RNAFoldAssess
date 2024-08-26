import os


from RNAFoldAssess.models import DataPoint
from RNAFoldAssess.models.scorers import *

approved_cohorts = [
    "C014G",
    "C014H",
    "C014I",
    "C014J",
    "C014U",
    "C014V"
]

headers = "algo_name, datapoint_name, sequence, prediction, accuracy, p_value"

dbn_base =  "/work/yesselmanlab/ewhiting/spot_outputs/ydata/dbn_files"

dp_file_path="/common/yesselmanlab/ewhiting/ss_deeplearning_data/data"

# for dpf in data_point_files:
#     cohort = dpf.split(".")[0]
#     if cohort not in approved_chorots:
#         continue
#     print(f"Loading data points from {cohort} cohort")
#     data_points += DataPoint.factory(f"{dp_file_path}/{dpf}", cohort)


report_file_path = f"/mnt/nrdstor/yesselmanlab/ewhiting/reports/ydata/SPOT-RNA_YesselmanDMS_report.txt"
report_file = open(report_file_path, "w")
for cohort in approved_cohorts:
    print(f"Working cohort {cohort}")
    datapoints = DataPoint.factory(f"{dp_file_path}/{cohort}.json", cohort)
    prediciton_dir = f"{dbn_base}/{cohort}"
    counter = 0
    for dp in datapoints:
        counter += 1
        if counter % 1250 == 0:
            print(f"Working {counter} of {cohort}")
        try:
            with open(f"{prediciton_dir}/{dp.name}.ct.dbn") as pf:
                pred_data = pf.readlines()
                dbn = pred_data[-1].strip()
            score = DSCI.score(
                dp.sequence,
                dbn,
                dp.reactivities,
                DMS=True
            )
            acc = score["accuracy"]
            p = score["p"]
            line = f"SPOT-RNA, {dp.name}, {dp.sequence}, {dbn}, {acc}, {p}\n"
            report_file.write(line)
        except Exception as e:
            print(f"Exception with {dp.name}: {e}")

report_file.close()
