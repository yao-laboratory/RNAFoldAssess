import os


models = ["ContextFold", "ContraFold", "EternaFold", "IPKnot",
          "NeuralFold", "NUPACK", "RNAFold",
          "RNAStructure", "pKnots", "Simfold",
          "MXFold", "MXFold2", "SPOT-RNA"]

pred_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/eterna_data/with_energy/canonical"

dps = set()

for m in models:
    with open(f"{pred_dir}/{m}_canonical_predictions.txt") as fh:
        lines = fh.readlines()
    
    lines = [line.split(", ") for line in lines]
    accs = [line[4] for line in lines]
    with open(f"scores/{m}_eterna_accs.txt", "w") as fh:
        fh.write(",".join(accs))

    datapoints = [line[1] for line in lines]
    for dp in datapoints:
        dps.add(dp)

dps = list(dps)
dp_map = {}
for dp in dps:
    dp_map[dp] = {}


for m in models:
    with open(f"{pred_dir}/{m}_canonical_predictions.txt") as fh:
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
    with open(f"scores/{m}_eterna_ordered_accs.txt", "w") as fh:
        fh.write(fstring)
