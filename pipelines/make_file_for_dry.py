import os, json


datapoint_path = "/common/yesselmanlab/ewhiting/ss_deeplearning_data/data"
report_path = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/ydata"

json_files = [
    "C014G.json",
    "C014H.json",
    "C014I.json",
    "C014J.json",
    "C014U.json",
    "C014V.json"
]
datapoints = {}

print("Assembling datapoints")
for jf in json_files:
    json_path = f"{datapoint_path}/{jf}"
    cohort = jf.split(".")[0]
    with open(json_path) as fh:
        dp_data = json.load(fh)

    for dp in dp_data:
        dp_name = f"{cohort}_{dp['name']}"
        seq = dp["sequence"]
        reactivities = dp["data"]
        stc = dp["structure"]
        datapoints[dp_name] = {
            "sequence": seq,
            "structure": stc,
            "reactivities": reactivities
        }

with open(f"{report_path}/all_ydata_rnas.json", "w") as fh:
    json.dump(datapoints, fh)

master_map = {}
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

print("Collecting model predictions")
for m in models:
    print(f"Working {m}")
    master_map[m] = {}
    report_file = f"{report_path}/{m}_YesselmanDMS_report.txt"
    with open(report_file) as fh:
        report_data = fh.readlines()

    if report_data[0].startswith("algo"):
        report_data.pop(0)

    report_data = [d.split(", ") for d in report_data]
    for rd in report_data:
        dp_name = rd[1]
        for item in rd[2:]:
            if item[0] in "().":
                pred = item
                break
        acc = float(rd[-2].strip())
        p = float(rd[-1])

        master_map[m][dp_name] = {
            "prediction": pred,
            "dsci_score": acc,
            "p_value": p,
        }

print("Writing data")
with open(f"{report_path}/all_predictions_by_model.json", "w") as fh:
    json.dump(master_map, fh)
