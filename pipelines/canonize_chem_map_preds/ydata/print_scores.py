import os


report_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/ydata/canonize"

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
    with open(f"{report_dir}/{m}_YesselmanDMS_report.txt") as fh:
        lines = fh.readlines()

    lines = [line.split(", ") for line in lines]
    accs = [float(line[4]) for line in lines]
    avg = sum(accs) / len(accs)
    print(f"{m} - {avg}, n = {len(accs)}")
