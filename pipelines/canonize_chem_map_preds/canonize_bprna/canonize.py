import os

from RNAFoldAssess.models import CanonicalBasePairScorer, BasePairScorer


base_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/bprna/acug_only_preds"
dest_dir = f"{base_dir}/canonical"

models = [
    # "ContextFold", # Done
    # "ContraFold", # Done
    "EternaFold",
    "IPKnot",
    # "NeuralFold", # Requires special handling
    "NUPACK",
    "RNAFold",
    "RNAStructure",
    "pKnots",
    # "Simfold", # Not present
    "MXFold",
    "MXFold2",
    # "SPOT-RNA" # Not present
]

headers = "algo_name, datapoint_name, lenience, sequence, true_structure, prediction, sensitivity, ppv, f1\n"
for m in models:
    print(f"Working {m}")
    fname = f"{m}_bpRNA-1m-90_all_report.txt"
    with open(f"{base_dir}/{fname}") as fh:
        lines = fh.readlines()
    
    if lines[0].startswith("model") or lines[0].startswith("algo"):
        lines.pop(0)

    fstring = headers
    for line in lines:
        line = line.split(", ")
        model = line[0]
        dp = line[1]
        lenience = int(line[2])
        seq = line[3]
        real_stc = line[4]
        real_stc = CanonicalBasePairScorer.transform_structure(real_stc, seq)
        pred_stc = line[5]
        pred_stc = CanonicalBasePairScorer.transform_structure(pred_stc, seq)
        score = BasePairScorer(real_stc, pred_stc, lenience)
        score.evaluate()
        s = score.sensitivity
        p = score.ppv
        f1 = score.f1
        new_line = f"{model}, {dp}, {lenience}, {seq}, {real_stc}, {pred_stc}, {s}, {p}, {f1}\n"
        fstring += new_line
    
    with open(f"{dest_dir}/{fname}", "w") as fh:
        fh.write(fstring)

print("Done")
