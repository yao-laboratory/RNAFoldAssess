import os


report_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/rasp_data/ara-tha"

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

all_pred_files = os.listdir(report_dir)

print("Making master file")
all_preds = []
for m in models:
    files = [f for f in all_pred_files if m in f]
    for f in files:
        with open(f"{report_dir}/{f}") as fh:
            lines = fh.readlines()
    
        if len(lines) <= 0:
            continue
            
        if lines[0].startswith("algo_name"):
            lines.pop(0)
    
    all_preds += lines

dest_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions"
with open(f"{dest_dir}/all_rasp_arabidopsis_preds.txt", "w") as fh:
    fh.write("".join(all_preds))
