import os


models = ["ContextFold", "ContraFold", "EternaFold", "IPKnot",
          "NeuralFold", "NUPACK", "RNAFold",
          "RNAStructure", "pKnots", "Simfold",
          "MXFold", "MXFold2", "SPOT-RNA"]

pred_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/crystal_release_2024/canonical"

dps = set()

leniences = [0, 1]
stat_key = {
    "sensitivity": 6,
    "ppv": 7,
    "f1": 8
}

for m in models:
    for lenience in leniences:
        with open(f"{pred_dir}/{m}_predictions_{lenience}_lenience.txt") as fh:
            lines = fh.readlines()
        
        if lines[0].startswith("algo"):
            lines.pop(0)
        
        lines = [line.split(", ") for line in lines]
        for stat, key in stat_key.items():
            accs = [line[key] for line in lines]
            with open(f"scores/pdb_scores/{m}_{stat}_{lenience}_lenience.txt", "w") as fh:
                fh.write(",".join(accs))

            datapoints = [line[1] for line in lines]
            for dp in datapoints:
                dps.add(dp)

dps = list(dps)
dp_map = {}
for dp in dps:
    dp_map[dp] = {}

for m in models:
    # Just use 1-lenience for this one
    with open(f"{pred_dir}/{m}_predictions_1_lenience.txt") as fh:
        lines = fh.readlines()
    
    if lines[0].startswith("algo"):
        lines.pop(0)
    
    lines = [line.split(", ") for line in lines]
    for line in lines:
        dp = line[1]
        dp_map[dp][m] = {}
        for stat, key in stat_key.items():
            acc = line[key]
            dp_map[dp][m][stat] = acc

matched = {}
for dp in dp_map:
    if not len(dp_map[dp]) == len(models):
        continue
    
    matched[dp] = dp_map[dp]

model_map = {}
for m in models:
    model_map[m] = {
        "sensitivity": [],
        "ppv": [],
        "f1": []
    }

for dp in matched:
    for m in models:
        for stat in stat_key:
            acc = matched[dp][m][stat]
            model_map[m][stat].append(acc)

for m in models:
    for stat in stat_key:
        accs = model_map[m][stat]
        fstring = ",".join(accs)
        with open(f"scores/pdb_scores/{m}_{stat}_ordered.txt", "w") as fh:
            fh.write(fstring)
