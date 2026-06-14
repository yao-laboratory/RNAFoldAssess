import os


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

report_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/rnandria/canonical"

for dt in ["pri_miRNA", "human_mRNA"]:
    print(f"{dt}")
    for m in models:
        with open(f"{report_dir}/{m}_{dt}_predictions.txt") as fh:
            pred_data = fh.readlines()

        pred_data = [pd.split(", ") for pd in pred_data]
        accs = [float(d[4]) for d in pred_data]
        avg = sum(accs) / len(accs)
        print(f"{m} - {avg}, n = {len(accs)}")
    print()
