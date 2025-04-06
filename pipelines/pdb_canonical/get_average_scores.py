base_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions"
models = [
    "ContextFold",
    "ContraFold",
    "EternaFold",
    "IPKnot",
    "MXFold",
    "MXFold2",
    "Neuralfold",
    "NUPACK",
    "pKnots",
    "RNAFold",
    "RNAStructure",
    "Simfold",
    "SPOT-RNA"
]


for lenience in [0, 1]:
    fname = f"{base_dir}/pdb_canonical_matched_{lenience}.txt"
    model_score_map = {}
    for m in models:
        model_score_map[m] = {"sensitivity": [], "ppv": [], "f1": []}

    with open(fname) as fh:
        data = [line.split(", ") for line in fh.readlines()]

    for d in data:
        model = d[0]
        if model == "RandomPredictor":
            continue
        s = float(d[5])
        p = float(d[6])
        f = float(d[7])
        model_score_map[model]["sensitivity"].append(s)
        model_score_map[model]["ppv"].append(p)
        model_score_map[model]["f1"].append(f)

    for m in models:
        scores = model_score_map[m]
        n = len(scores['sensitivity'])
        line = f"Lenience {lenience}, {m}: "
        line += f"{n}, "
        line += f"{sum(scores['sensitivity'])/n},"
        line += f"{sum(scores['ppv'])/n},"
        line += f"{sum(scores['f1'])/n}"
        print(line)
