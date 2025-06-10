import os


report_dir = "/work/yesselmanlab/ewhiting/bprna_canonical_reports/acug_preds"

files = os.listdir(report_dir)

lenience_index = 2
sens_index = 6
ppv_index = 7
f1_index = 8

for f in files:
    with open(f"{report_dir}/{f}") as fh:
        preds = fh.readlines()
    
    preds = [pred.split(", ") for pred in preds]
    lenience = preds[0][lenience_index]
    model = f.split("_")[0]

    sens = [float(line[sens_index]) for line in preds]
    ppvs = [float(line[ppv_index]) for line in preds]
    f1s = [float(line[f1_index]) for line in preds]

    n = len(sens)

    sen = sum(sens) / n
    ppv = sum(ppvs) / n
    f1 = sum(f1s) / n

    print(f"{model} - {lenience}:")
    print(f"{n},{sen},{ppv},{f1}")
    
