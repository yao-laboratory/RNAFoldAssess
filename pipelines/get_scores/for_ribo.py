import os


models = ["ContextFold", "ContraFold", "EternaFold", "IPKnot",
          "NeuralFold", "NUPACK", "RNAFold",
          "RNAStructure", "pKnots", "Simfold",
          "MXFold", "MXFold2", "SPOT-RNA"]

pred_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/ribonanza/canonical"

dps = set()

for m in models:
    pred_files = [f for f in os.listdir(pred_dir) if f"{m}_" in f]
    accs = []
    for pf in pred_files:
        with open(f"{pred_dir}/{pf}") as fh:
            lines = fh.readlines()
        
        lines = [line.split(", ") for line in lines]
        f_accs = [line[4] for line in lines]
        accs += f_accs

        f_dps = [line[1] for line in lines]
        for fdp in f_dps:
            dps.add(fdp)
    
    with open(f"scores/ribonanza_scores/{m}_ribo_accs.txt", "w") as fh:
        fh.write(",".join(accs))

dps = list(dps)
dp_map = {}
for dp in dps:
    dp_map[dp] = {}

for m in models:
    pred_files = [f for f in os.listdir(pred_dir) if f"{m}_" in f]
    for pf in pred_files:
        with open(f"{pred_dir}/{pf}") as fh:
            lines = fh.readlines()
        
        lines = [line.split(", ") for line in lines]
        for line in lines:
            dp = line[1]
            acc = line[4]
            dp_map[dp][m] = acc


matched = {}
for dp in dp_map:
    if not len(dp_map[dp]) == len(models):
        continue
    
    matched[dp] = dp_map[dp]

model_map = {}
for m in models:
    model_map[m] = []

for dp in matched:
    for m in models:
        acc = matched[dp][m]
        model_map[m].append(acc)

for m, accs in model_map.items():
    fstring = ",".join(accs)
    with open(f"scores/ribonanza_scores/{m}_ribo_ordered_accs.txt", "w") as fh:
        fh.write(fstring)
