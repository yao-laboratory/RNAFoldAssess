import os


models = [
    "ContextFold",
    "ContraFold",
    "EternaFold",
    "RandomPredictor",
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

# Get all datapoints
ribo_data_csv = "/mnt/nrdstor/yesselmanlab/ewhiting/rna_data/ribonanza/rmdb_data.v1.3.0.csv"
f = open(ribo_data_csv)
data = f.readlines()
f.close()
data.pop(0)
data = [d.split(",") for d in data]
all_dps = [d[0] for d in data]

destination_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/ribonanza/remaining_dps"
existing_report_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/ribonanza/unique_preds"

for model in models:
    # Get predicted datapoints
    existing_report = f"{existing_report_dir}/{model}_unique_predictions.txt"
    with open(existing_report) as fh:
        predictions = [d.split(", ") for d in fh.readlines()]
    predicted_dps = [d[1] for d in predictions]

    # Find missing ribonanza datapoints
    missing_dps = set()
    for dp in all_dps:
        if dp not in predicted_dps:
            missing_dps.add(dp)

    print(f"{model}: {len(missing_dps)} missing datapoints")

    with open(f"{destination_dir}/{model}_missing_dps.txt", "w") as fh:
        for md in missing_dps:
            fh.write(f"{md}\n")

