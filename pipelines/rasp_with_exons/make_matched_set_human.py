import os

base_report_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/rasp_data"
species = "human"
report_dir = f"{base_report_dir}/{species}/fixed_files"
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

dp_model_map = {}

print("Assembling datapoints")
files = os.listdir(report_dir)
for f in files:
    with open(f"{report_dir}/{f}") as fh:
        data = fh.readlines()
    
    m = f.split("_")[0]
    if len(data) <= 0:
        continue

    if data[0].startswith("algo"):
        data.pop(0)
    
    data = [d.split(", ") for d in data]
    for d in data:
        dp = d[1]
        seq = d[2]
        pred = d[3]
        try:
            dp_model_map[dp].append(m)
        except KeyError:
            dp_model_map[dp] = [m]

print("Preparing file string")
matched_set = []
for f in files:
        with open(f"{report_dir}/{f}") as fh:
            data = fh.readlines()
        
        if len(data) <= 0:
            continue

        if data[0].startswith("algo"):
            data.pop(0)
        
        for datum in data:
            spl = datum.split(", ")
            dp_name = spl[1]
            preds = dp_model_map[dp_name]
            anomalies = 0
            if len(preds) >= len(models):
                matched_set.append(datum)
                if len(preds) > len(models):
                    anomalies += 1

print(f"File string prepared. {anomalies} anomalies found")

dest_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions"
print(f"Writing matched set ({len(matched_set)} predictions)")
with open(f"{dest_dir}/rasp_matched_set", "w") as fh:
    fh.write("".join(matched_set))

