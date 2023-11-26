import os, csv

from RNAFoldAssess.utils import *

# Original pipeline broke. Data was gathered but the analysis broke. Just redoing it here.

model_name = "MXFold"
data_type_name = "bpRNA-1m-90"
analysis_report_path = f"/common/yesselmanlab/ewhiting/reports/{model_name}_{data_type_name}_report.txt"

f = open(analysis_report_path)
reader = csv.DictReader(f)
rows = []
for row in reader:
    rows.append(row)

f.close()
del(reader)

sensitivities = {}
ppvs = {}
f1s = {}
lowest_sensitivity = {}
lowest_ppv = {}
lowest_f1 = {}
leniences = [0, 1]
for lenience in leniences:
    sensitivities[f"{lenience}"] = []
    ppvs[f"{lenience}"] = []
    f1s[f"{lenience}"] = []
    lowest_sensitivity[f"{lenience}"] = [1.0, ""]
    lowest_ppv[f"{lenience}"] = [1.0, ""]
    lowest_f1[f"{lenience}"] = [1.0, ""]

count_of_rows = len(rows)
counter = 0

print(f"Starting analysis on {count_of_rows} datapoints ...")

for r in rows:
    counter += 1
    if counter % 250 == 0:
        print(f"Working on {counter} of {count_of_rows}")
    name = r[" datapoint_name"].strip()
    for lenience in leniences:
        if int(r[" lenience"].strip()) == lenience:
            s = float(r[" sensitivity"].strip())
            p = float(r[" ppv"].strip())
            f1 = float(r[" F1"].strip())
            sensitivities[f"{lenience}"].append(s)
            ppvs[f"{lenience}"].append(p)
            f1s[f"{lenience}"].append(f1)

            if s < lowest_sensitivity[f"{lenience}"][0]:
                lowest_sensitivity[f"{lenience}"][0] = s
                lowest_sensitivity[f"{lenience}"][1] = name

            if p < lowest_ppv[f"{lenience}"][0]:
                lowest_ppv[f"{lenience}"][0] = p
                lowest_ppv[f"{lenience}"][1] = name

            if f1 < lowest_f1[f"{lenience}"][0]:
                lowest_f1[f"{lenience}"][0] = f1
                lowest_f1[f"{lenience}"][1] = name


pipeline_report_path = f"/common/yesselmanlab/ewhiting/reports/{model_name}_{data_type_name}.txt"
write_bp_pipeline_report(
    pipeline_report_path,
    count_of_rows,
    leniences,
    sensitivities,
    lowest_sensitivity,
    ppvs,
    lowest_ppv,
    f1s,
    lowest_f1
)
