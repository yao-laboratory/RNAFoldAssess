import os


base_path = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/rasp_data/HIV"

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

dp_preds = {}

for m in models:
    report_dir = f"{base_path}/{m}"
    files = [f for f in os.listdir(report_dir) if f.endswith("_predictions.txt")]
    for pred_file in files:
        with open(f"{report_dir}/{pred_file}") as fh:
            data = fh.readlines()

        # Remove header
        if data[0].startswith("algo"):
            data.pop(0)

        data = [d.split(", ") for d in data]
        for d in data:
            dp = d[1]
            acc = d[4]

            try:
                dp_preds[dp][m] = acc
            except KeyError:
                dp_preds[dp] = {m: acc}

matched_set = []
unmatched_set = []

for dp, predictions in dp_preds.items():
    if len(predictions) != len(models):
        unmatched_set.append(dp)
    else:
        matched_set.append(dp)


print(f"There are {len(matched_set)} of {len(dp_preds)} datapoints predicted by all models")

model_count = {}
for m in models:
    model_count[m] = 0

for dp, predictions in dp_preds.items():
    for m in models:
        if m in predictions:
            model_count[m] += 1

for m, c in model_count.items():
    print(f"{m}: {c}")

ordered_model_preds = {}
for m in models:
    ordered_model_preds[m] = []

print()

# Make ordered predictions
for dp in matched_set:
    for m in models:
        acc = dp_preds[dp][m]
        ordered_model_preds[m].append(acc)

print(f'Writing acc files')

for m, accs in ordered_model_preds.items():
    fstring = ",".join(accs)
    with open(f"{m}_hiv_accs.txt", "w") as fh:
        fh.write(fstring)

print("done")
