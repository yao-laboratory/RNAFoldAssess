import os
import pandas as pd


base_dir = "/common/yesselmanlab/ewhiting/reports/rasp_data"

def get_prediction_files(model_name, species):
    predictions_dir = f"{base_dir}/{species}/{model_name}/filtered"
    all_files = os.listdir(predictions_dir)
    files = [f"{predictions_dir}/{f}" for f in all_files if f.endswith("predictions.txt")]
    return files

accuracies = []
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

rasp_folders = [
    "arabidopsis",
    "covid", # Skipping COVID because it had no bad guesses?
    "ecoli",
    "HIV",
    "human"
]

species_accs = {}
for s in rasp_folders:
    species_accs[s] = []

print("Getting accuracies")
for folder in rasp_folders:
    for m in models:
        print(m)
        files = get_prediction_files(m, folder)
        for f in files:
            print(f"\t- {f}")
            file = open(f)
            data = file.readlines()
            file.close()
            if data == []:
                continue
            # Get rid of header
            data.pop(0)
            for d in data:
                acc = float(d.split(", ")[4])
                accuracies.append(acc)
                species_accs[folder].append(acc)



all_series = pd.Series(accuracies)
descriptive_stats = all_series.describe()

lo_cutoff = descriptive_stats["25%"]
hi_cutoff = descriptive_stats["75%"]


destination_dir = "/common/yesselmanlab/ewhiting/dataset_analyses/rasp/filtered"
species_files = {}
for s in species_accs:
    accs = species_accs[s]
    series = pd.Series(accs)
    stats = series.describe()
    species_lo_cutoff = stats["25%"]
    species_hi_cutoff = stats["75%"]
    species_files[s] = {
        "low_cutoff": species_lo_cutoff,
        "high_cutoff": species_hi_cutoff,
        "low": open(f"{destination_dir}/{s}_low_preds.txt", "w"),
        "mid": open(f"{destination_dir}/{s}_mid_preds.txt", "w"),
        "high": open(f"{destination_dir}/{s}_high_preds.txt", "w")
    }


good_guesses = open(f"{destination_dir}/RASP_good_guesses.txt", "w")
bad_guesses = open(f"{destination_dir}/RASP_bad_guesses.txt", "w")
mid_guesses = open(f"{destination_dir}/RASP_mid_guesses.txt", "w")

model_performance = {}
for m in models:
    model_performance[m] = {"low": 0, "mid": 0, "hi": 0}
    for s in species_files:
        model_performance[m][s] = {"low": 0, "mid": 0, "hi": 0}

print("Evaluating models")
for folder in rasp_folders:
    species_lo_cutoff = species_files[folder]["low_cutoff"]
    species_hi_cutoff = species_files[folder]["high_cutoff"]
    species_bad_guesses = species_files[folder]["low"]
    species_mid_guesses = species_files[folder]["mid"]
    species_good_guesses = species_files[folder]["high"]
    for m in models:
        files = get_prediction_files(m, folder)
        print(m)
        for f in files:
            print(f"\t- {f}")
            file = open(f)
            data = file.readlines()
            file.close()
            if data == []:
                continue
            # Get rid of header
            data.pop(0)
            for d in data:
                acc = float(d.split(", ")[4])
                if acc <= lo_cutoff:
                  bad_guesses.write(d)
                  model_performance[m]["low"] += 1
                elif acc >= hi_cutoff:
                    model_performance[m]["hi"] += 1
                    good_guesses.write(d)
                else:
                    model_performance[m]["mid"] += 1
                    mid_guesses.write(d)

                if acc <= species_lo_cutoff:
                    model_performance[m][folder]["low"] += 1
                    species_bad_guesses.write(d)
                elif acc >= species_hi_cutoff:
                    model_performance[m][folder]["hi"] += 1
                    species_good_guesses.write(d)
                else:
                    model_performance[m][folder]["mid"] += 1
                    species_mid_guesses.write(d)



good_guesses.close()
bad_guesses.close()

for s in species_files:
    files = species_files[s]
    files["low"].close()
    files["mid"].close()
    files["high"].close()

print("Writing main evaluation")

perf_file = open("RASP_data_model_performance.txt", "w")
line = "Model\tLow\tHigh\tMid\n"
for mp in model_performance:
    perf = model_performance[mp]
    line += f"{mp}\t"
    line += f"{perf['low']}\t"
    line += f"{perf['hi']}\t"
    line += f"{perf['mid']}\n"

perf_file.write(line)
perf_file.close()

print("Writing species evaluations")

for s in rasp_folders:
    line = "Model\tLow\tHigh\tMid\n"
    species_perf_file = open(f"RASP_{s}_data_model_performance.txt", "w")
    print(f"\t - {s}")
    for mp in model_performance:
        species_perf = model_performance[mp][s]
        line += f"{mp}\t"
        line += f"{species_perf['low']}\t"
        line += f"{species_perf['hi']}\t"
        line += f"{species_perf['mid']}\n"
    species_perf_file.write(line)
    species_perf_file.close()

print("Done")
