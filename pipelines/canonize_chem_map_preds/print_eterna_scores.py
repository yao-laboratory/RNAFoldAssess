import os


report_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/eterna_data/with_energy/canonical"

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

for m in models:
    with open(f"{report_dir}/{m}_canonical_predictions.txt") as fh:
        preds = fh.readlines()

    preds = [p.split(", ") for p in preds]
    accs = [float(d[4]) for d in preds]
    print(f"{m} - {sum(accs) / len(accs)}, n = {len(accs)}")
