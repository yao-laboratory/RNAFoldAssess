import os


models = {
    "ContraFold",
    "CFRetrainedEterna",
    "CFRetrainedRibonanza",
    "CFRetrainedRNAndria",
    "ContraRetrainedYData",
    "MXFold2",
    "MXFold2RetrainedEterna",
    "MXFold2RetrainedRibonanza",
    "MXFold2RetrainedRNAndria",
    "MXFold2RetrainedYData"
}

# Just do Ribo for now
report_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/ribonanza/with_energies"

model_preds = {}
for m in models:
    relevant_files = [f for f in os.listdir(report_dir) if f"{m}_" in f and "predictions.txt" in f]
    data = []
    for rf in relevant_files:
        # 4
        with open(f"{report_dir}/{rf}") as fh:
            lines = [d.split(", ") for d in fh.readlines()]
        data += [float(i[4]) for i in lines]
    model_preds[m] = data

for model, accs in model_preds.items():
    with open(f"{model}_ribo_accs.txt", "w") as fh:
        fh.write(",".join([str(i) for i in accs]))
