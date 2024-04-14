import os


import pandas as pd

base_dir = "/common/yesselmanlab/ewhiting/reports/rnandria"

def pri_file_name(model_name):
    return f"{base_dir}/{model_name}_rnandria_pri_miRNA_predictions.txt"

def human_file_name(model_name):
    return f"{base_dir}/{model_name}_rnandria_human_mRNA_predictions.txt"

destination_base = "/common/yesselmanlab/ewhiting/reports/rnandria/analyses"
pri_destination = f"{destination_base}/pri"
human_destination = f"{destination_dir}/human"

all_accuracies = []
pri_accuracies = []
human_accuracies = []
models = [
    "ContextFold",
    "ContraFold",
    "EternaFold",
    "IPKnot",
    "MXFold",
    "RandomPredictor",
    "RNAFold",
    "SeqFold"
]

for m in models:
    # Get pri miRNA predictions
    pri_path = pri_file_name(m)
    pf = open(pri_path)
    data = pf.readlines()
    pf.close()
    # Get rid of headers
    if data == []:
        continue
    data.pop(0)
    for d in data:
        acc = float(d.split(", ")[4])
        all_accuracies.append(acc)
        pri_accuracies.append(acc)
    # Get human predictions
    human_path = human_file_name(m)
    hf = open(human_path)
    data = hf.readlines()
    hf.close()
    # Get rid of headers
    if data == []:
        continue
    data.pop(0)
    for d in data:
        acc = float(d.split(", ")[4])
        all_accuracies.append(acc)
        human_accuracies.append(acc)

all_s = pd.Series(all_accuracies)
pri_s = pd.Series(pri_accuracies)
human_s = pd.Series(human_accuracies)

all_stats = all_s.describe()
pri_stats = pri_s.describe()
human_stats = human_s.describe()

f = open(f"{destination_base}/all_accuracies_stats.txt", "w")
w.write(str(all_stats))
f.close()

f = open(f"{destination_base}/pri_accuracies_stats.txt", "w")
w.write(str(pri_stats))
f.close()

f = open(f"{destination_base}/human_accuracies_stats.txt", "w")
w.write(str(human_stats))
f.close()


lo_cutoff = all_stats["25%"]
hi_cutoff = all_stats["75%"]

pri_lo_cutoff = pri_stats["25%"]
pri_hi_cutoff = pri_stats["75%"]

human_lo_cutoff = human_stats["25%"]
human_hi_cutoff = human_stats["75%"]

model_perf = {}
for m in models:
    model_perf[m] = {
        "all_low": 0,
        "all_mid": 0,
        "all_high": 0,
        "pri_low": 0,
        "pri_mid": 0,
        "pri_high": 0,
        "human_low": 0,
        "human_mid": 0
        "human_high": 0
    }

all_lo_preds = []
all_hi_preds = []
pri_lo_preds = []
pri_hi_preds = []
hum_lo_preds = []
hum_hi_preds = []

for m in models:
    # Get pri miRNA predictions
    pri_path = pri_file_name(m)
    pf = open(pri_path)
    data = pf.readlines()
    pf.close()
    # Get rid of headers
    if data == []:
        continue
    data.pop(0)
    for d in data:
        items = d.split(", ")
        acc = items[4]
        if acc <= lo_cutoff:
            all_lo_preds.append(d)
            model_perf[m]["all_low"] += 1
        elif acc >= hi_cutoff:
            all_hi_preds.append(d)
            model_perf[m]["all_high"] += 1
        else:
            model_perf[m]["all_mid"] += 1

        if acc <= pri_lo_cutoff:
            pri_lo_preds.append(d)
            model_perf[m]["pri_low"] += 1
        elif acc >= pri_hi_cutoff:
            pri_hi_preds.append(d)
            model_perf[m]["pri_high"] += 1
        else:
            model_perf[m]["pri_mid"] += 1

        if acc <= human_lo_cutoff:
            hum_lo_preds.append(d)
            model_perf[m]["human_low"] += 1
        elif acc >= human_hi_cutoff:
            hum_hi_preds.append(d)
            model_perf[m]["human_high"] += 1
        else:
            model_perf[m]["human_mid"] += 1


def write_predictions(predictions, file_path):
    f = open(file_path, "w")
    for p in predictions:
        f.write(p)
    f.close()

destination_base = "/common/yesselmanlab/ewhiting/reports/rnandria/analyses"
pri_destination = f"{destination_base}/pri"
human_destination = f"{destination_dir}/human"

write_predictions(all_lo_preds, f"{destination_base}/all_low_predictions.txt")
write_predictions(all_lo_preds, f"{pri_destination}/pri_miRNA_low_predictions.txt")
write_predictions(all_lo_preds, f"{human_destination}/human_mRNA_predictions.txt")

def write_model_perf(location, prefix):
    line = "model, low, high, middle\n"
    for m in model_perf:
        low = model_perf[m][f"{prefix}_low"]
        mid = model_perf[m][f"{prefix}_mid"]
        high = model_perf[m][f"{prefix}_high"]
        line += f"{m}\t{low}\t{mid}\t{high}\n"
    f = open(location, "w")
    f.write(line)
