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

dest_dir = "/home/yesselmanlab/ewhiting/RNAFoldAssess/files_for_figures/bprna"


for lenience in [0, 1]:
    matched_file = f"/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions/bprna_matched_set_{lenience}.txt"
    model_map = {}

    for m in models:
        model_map[m] = {"sens": [], "ppv": [], "f1": []}

    # 7, 8, 9

    with open(matched_file) as fh:
        data = [d.split(", ") for d in fh.readlines()]

    counter = 0
    len_data = len(data)
    for d in data:
        counter += 1
        if counter % 1000 == 0:
            print(f"Working {counter} of {len_data}")
        model = d[1]
        if model == "RandomPredictor":
            continue
        s = float(d[7])
        p = float(d[8])
        f = float(d[9])
        model_map[model]["sens"].append(s)
        model_map[model]["ppv"].append(p)
        model_map[model]["f1"].append(f)


    for m, stats in model_map.items():
        for stat in ["sens", "ppv", "f1"]:
            values = stats[stat]
            with open(f"{dest_dir}/{m}_{stat}_{lenience}_lenience.txt", "w") as fh:
                fh.write(",".join([str(i) for i in values]))
