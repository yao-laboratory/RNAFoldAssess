import os


base_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions"

models = [
    "ContextFold",
    "ContraFold",
    "EternaFold",
    "IPKnot",
    "MXFold",
    "MXFold2",
    "NeuralFold",
    "NUPACK",
    "pKnots",
    "RNAFold",
    "RNAStructure",
    "Simfold",
    "SPOT-RNA"
]


for lenience in [0,1]:
    model_dp_map = {}
    for m in models:
        model_dp_map[m] = []

    fpath = f"{base_dir}/bprna_matched_set_{lenience}.txt"
    with open(fpath) as fh:
        data = [line.split(", ") for line in fh.readlines()]

    for d in data:
        model = d[0]
        dp = d[1]
        model_dp_map[model].append(dp)


    for m, dps in model_dp_map.items():
        print(f"{m} - {len(dps):,}")
