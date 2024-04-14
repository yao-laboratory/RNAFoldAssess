import os

import pandas as pd


base_dir = "/common/yesselmanlab/ewhiting/reports/bprna"

no_lenience_sensitivities = []
one_bp_lenience_sensitivities = []
models = [
    "ContextFold",
    "ContraFold",
    "EternaFold",
    "IPknot",
    "MXFold",
    "RandomPredictor",
    "RNAFold",
    "SeqFold"
]

files = [f"{base_dir}/{m}_bpRNA-1m-90_report.txt" for m in models]

model_perf_no_leneince = {}
model_perf_1bp_lenience = {}
for m in models:
    model_perf_no_leneince[m] = {"low": 0, "mid": 0, "high": 0}
    model_perf_1bp_lenience[m] = {"low": 0, "mid": 0, "high": 0}


for fi in files:
    f = open(fi)
    data = f.readlines()
    f.close()
    for d in data:
        items = d.split(", ")
        lenience = items[2]
        sensitivity = float(items[5])
        if int(lenience) == 0:
            no_lenience_sensitivities.append(sensitivity)
        else:
            one_bp_lenience_sensitivities.append(sensitivity)

lenience0_sens = pd.Series(no_lenience_sensitivities)
leneince1_sens = pd.Series(one_bp_lenience_sensitivities)

ds0 = lenience0_sens.describe()
ds1 = leneince1_sens.describe()

ds0_lo_cutoff = ds0["25%"]
ds0_hi_cutoff = ds0["75%"]
ds1_lo_cutoff = ds1["25%"]
ds1_hi_cutoff = ds1["75%"]

destination_dir = "/common/yesselmanlab/ewhiting/reports/bprna/ranked"
ds0_hi_dest = open(f"{destination_dir}/bpRNA_len0_hi_prediction.txt", "w")
ds0_mid_dest = open(f"{destination_dir}/bpRNA_len0_mid_prediction.txt", "w")
ds0_lo_dest = open(f"{destination_dir}/bpRNA_len0_lo_prediction.txt", "w")
ds1_hi_dest = open(f"{destination_dir}/bpRNA_len1_hi_prediction.txt", "w")
ds1_mid_dest = open(f"{destination_dir}/bpRNA_len1_mid_prediction.txt", "w")
ds1_lo_dest = open(f"{destination_dir}/bpRNA_len1_lo_prediction.txt", "w")

for m in models:
    f = open(f"{base_dir}/{m}_bpRNA-1m-90_report.txt")
    data = f.readlines()
    f.close()
    for d in data:
        items = d.split(", ")
        lenience = items[2]
        sensitivity = float(items[5])
        if int(lenience) == 0:
            if sensitivity <= ds0_lo_cutoff:
                ds0_lo_dest.write(d)
                model_perf_no_leneince[m]["low"] += 1
            elif sensitivity >= ds0_hi_cutoff:
                ds0_hi_dest.write(d)
                model_perf_no_leneince[m]["high"] += 1
            else:
                ds0_mid_dest.write(d)
                model_perf_no_leneince[m]["mid"] += 1
        else:
            if sensitivity <= ds1_lo_cutoff:
                ds1_lo_dest.write(d)
                model_perf_1bp_lenience[m]["low"] += 1
            elif sensitivity >= ds1_hi_cutoff:
                ds1_hi_dest.write(d)
                model_perf_1bp_lenience[m]["high"] += 1
            else:
                ds1_mid_dest.write(d)
                model_perf_1bp_lenience[m]["mid"] += 1


f0 = open("model_perf_no_lenience.txt","w")
line = "model, low, high, mid\n"
for m in model_perf_no_leneince:
    line += f"{m}\t{model_perf_no_leneince[m]['low']}\t{model_perf_no_leneince[m]['high']}\t{model_perf_no_leneince[m]['mid']}\n"

f0.write(line)
f0.close()

f1 = open("model_perf_1bp_lenience.txt", "w")
line = "model, low, high, mid\n"
for m in model_perf_1bp_lenience:
    line += f"{m}\t{model_perf_1bp_lenience[m]['low']}\t{model_perf_1bp_lenience[m]['high']}\t{model_perf_1bp_lenience[m]['mid']}\n"
f1.write(line)
f1.close()
