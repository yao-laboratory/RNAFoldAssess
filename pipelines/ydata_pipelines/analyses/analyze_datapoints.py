import os


low_quartile = 0.8778
high_quartile = 0.9792

def report_file(model_name):
    return f"/common/yesselmanlab/ewhiting/reports/ydata/{model_name}_YesselmanDMS_report.txt"


model_names = [
    "ContextFold",
    "ContraFold",
    "EternaFold",
    "IPknot",
    "MXFold",
    "RandomPredictor",
    "RNAFold",
    "SeqFold"
]

models_count = len(model_names)

model_predict_performance = {}
for m in model_names:
    model_predict_performance[m] = {"good": 0, "bad": 0, "mid": 0}

data_points = {}
for m in model_names:
    file = open(report_file(m))
    data = file.readlines()
    file.close()
    # Remove header
    data.pop(0)
    for d in data:
        d = d.split(", ")
        model = d[0]
        dp_name = d[1]
        acc = float(d[4])
        acc_range = ""
        if acc <= low_quartile:
            acc_range = "LOWEST"
        elif acc >= high_quartile:
            acc_range = "HIGHEST"
        else:
            acc_range = "MID"
        try:
            if acc_range == "LOWEST":
                data_points[dp_name]["lowest"] += 1
                data_points[dp_name]["lowest_preds"].append(d)
                model_predict_performance[m]["bad"] += 1
            elif acc_range == "HIGHEST":
                data_points[dp_name]["highest"] += 1
                data_points[dp_name]["highest_preds"].append(d)
                model_predict_performance[m]["good"] += 1
            else:
                data_points[dp_name]["mid"] += 1
                data_points[dp_name]["mid_preds"].append(d)
                model_predict_performance[m]["mid"] += 1
        except KeyError:
            data_points[dp_name] = {
                "lowest": 0,
                "mid": 0,
                "highest": 0,
                "sequence": d[2],
                "lowest_preds": [],
                "highest_preds": [],
                "mid_preds": []
            }
            if acc_range == "LOWEST":
                data_points[dp_name]["lowest"] += 1
                data_points[dp_name]["lowest_preds"].append(d)
                model_predict_performance[m]["bad"] += 1
            elif acc_range == "HIGHEST":
                data_points[dp_name]["highest"] += 1
                data_points[dp_name]["highest_preds"].append(d)
                model_predict_performance[m]["good"] += 1
            else:
                data_points[dp_name]["mid"] += 1
                data_points[dp_name]["mid_preds"].append(d)
                model_predict_performance[m]["mid"] += 1

analyses_path = "/common/yesselmanlab/ewhiting/reports/ydata/analyses"
all_bad_guesses_report = f"{analyses_path}/all_bad_guesses.txt"
all_good_guesses_report = f"{analyses_path}/all_good_guesses.txt"
abgr = open(all_bad_guesses_report, "w")
aggr = open(all_good_guesses_report, "w")


consistently_bad = []
consistently_good = []

for data_point in data_points:
    dp = data_points[data_point]
    for bg in dp["lowest_preds"]:
        abgr.write(", ".join(bg))
    for gg in dp["highest_preds"]:
        aggr.write(", ".join(gg))
    if dp["lowest"] / models_count >= 0.75:
        consistently_bad.append((data_point, dp["sequence"]))
    elif dp["highest"] / models_count >= 0.75:
        consistently_good.append((data_point, dp["sequence"]))

print(len(consistently_bad))
print(len(consistently_good))
for m in model_predict_performance:
    print(f"{m}: good: {model_predict_performance[m]['good']} med: {model_predict_performance[m]['mid']} bad: {model_predict_performance[m]['bad']}")



bad_dps_file = open(f"{analyses_path}/consistently_bad_datapoints.txt", "w")
for cb in consistently_bad:
    bad_dps_file.write(f"{cb[0]}, {cb[1]}\n")
bad_dps_file.close()
good_dps_file = open(f"{analyses_path}/consistently_good_datapoints.txt", "w")
for cg in consistently_good:
    good_dps_file.write(f"{cg[0]}, {cg[1]}\n")
good_dps_file.close()

