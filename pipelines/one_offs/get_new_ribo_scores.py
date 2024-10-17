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

report_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/ribonanza/unique_preds"

for m in models:
    datapoints = []
    accs = []
    with open(f"{report_dir}/{m}_unique_predictions.txt") as fh:
        data = fh.readlines()
    data = [d.split(", ") for d in data]
    for d in data:
        dp = d[1]
        if dp in datapoints:
            raise Exception(f"Duplicate found in {m} prediciton file: {dp}")
        else:
            datapoints.append(dp)
        accs.append(float(d[4]))
    print(f"{m}: {sum(accs) / len(accs)}")
