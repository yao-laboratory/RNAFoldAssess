import os, datetime

import pandas as pd

model_name = "MXFold"
chemical_mapping_method = "SHAPE"
species = "covid"


data = f"/common/yesselmanlab/ewhiting/data/rasp_data/processed/{species}"
json_files = os.listdir(data)

all_acc_scores = []
all_p_vals = []
all_perfect_score_count = 0

for jf in json_files:
    acc_scores = []
    p_vals = []
    perfect_score_count = 0
    file_prefix = jf.split(".")[0]
    generated_report_path = f"/common/yesselmanlab/ewhiting/reports/rasp_data/{species}/{model_name}_{file_prefix}_predictions.txt"
    f = open(generated_report_path)
    data = f.readlines()
    f.close()
    # Remove headers
    data.pop(0)
    if len(data) > 0:
        for prediction in data:
            prediction = prediction.split(", ")
            acc = float(prediction[-2])
            if acc == 1.0:
                perfect_score_count += 1
            p = float(prediction[-1])
            acc_scores.append(acc)
            p_vals.append(p)
        avg_p_val = sum(p_vals) / len(p_vals)
        s = pd.Series(acc_scores)
        descriptive_stats = s.describe()
        report = f"{model_name} evaluation on RASP data for {species} species in file {file_prefix}\n"
        report += f"Evaluated {len(acc_scores)} data points\n"
        report += f"Using DSCI, {perfect_score_count} predictions achieved a perfect score\n"
        report += f"Descriptive statistics:\n"
        report += f"{descriptive_stats}\n"
        report += f"\nReport generated on: {datetime.datetime.now()}\n\n"
        report_path = f"/common/yesselmanlab/ewhiting/reports/rasp_data/{species}/{model_name}_{file_prefix}_summary.txt"
        f = open(report_path, "w")
        f.write(report)
        f.close()

        all_acc_scores += acc_scores
        all_p_vals += p_vals
        all_perfect_score_count += perfect_score_count



all_avg_p_val = sum(all_p_vals) / len(all_p_vals)
all_s = pd.Series(all_acc_scores)
all_descriptive_stats = all_s.describe()

report = f"{model_name} evaluation on RASP data for {species} species\n"
report += f"Evaluated {len(all_acc_scores)} data points\n"
report += f"Using DSCI, {all_perfect_score_count} predictions achieved a perfect score\n"
report += f"Descriptive statistics:\n"
report += f"{all_descriptive_stats}\n"
report += f"\nReport generated on: {datetime.datetime.now()}\n\n"

report_path = f"/common/yesselmanlab/ewhiting/reports/rasp_data/{species}/{model_name}_{species}_all_summary.txt"
f = open(report_path, "w")
f.write(report)
f.close()
