import os


models = ["ContextFold", "ContraFold", "EternaFold", "IPKnot",
          "NeuralFold", "NUPACK", "RNAFold",
          "RNAStructure", "pKnots", "Simfold",
          "MXFold", "MXFold2", "SPOT-RNA"]

species = ["human", "covid", "HIV", "ecoli"] # and ara-tha but that's not done yet

base_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/consolidated"
for s in species:
    print(f"Working {s}")
    dps = set()
    model_accs = {}
    for m in models:
        model_accs[m] = []
    
    file_loc = f"{base_dir}/RASP_{s}_canonical_preds.txt"
    with open(file_loc) as fh:
        lines = fh.readlines()
    lines = [line.split(", ") for line in lines]

    for line in lines:
        dp = line[1]
        dps.add(dp)
        model = line[2]
        acc = line[5]
        model_accs[model].append(acc)
    
    for m in models:
        fstring = ",".join(model_accs[m])
        with open(f"acc_dir/{m}_{s}_accs.txt", "w") as fh:
            fh.write(fstring)
        
    dps = list(dps)
    dp_model_map = {}
    for dp in dps:
        dp_model_map[dp] = {}
    
    for line in lines:
        dp = line[1]
        model = line[2]
        acc = line[5]
        dp_model_map[dp][model] = acc
    
    print("Collecting matched accs")
    matched_set = {}
    for dp in dp_model_map:
        if not len(dp_model_map[dp]) == len(models):
            continue
        
        matched_set[dp] = dp_model_map[dp]
    
    model_map = {}
    for m in models:
        model_map[m] = []
    
    for dp in matched_set:
        for m in models:
            acc = matched_set[dp][m]
            model_map[m].append(acc)
    
    for m, accs in model_map.items():
        fstring = ",".join(accs)
        with open(f"acc_dir/{m}_{s}_ordered_accs.txt", "w") as fh:
            fh.write(fstring)
    
print("Done")
