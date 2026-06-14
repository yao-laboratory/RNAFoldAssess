import os

from RNAFoldAssess.models import CanonicalBasePairScorer, BasePairScorer


base_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/crystal_release_2024"
dest_dir = f"{base_dir}/canonical"

models = [
        #  "ContextFold", "ContraFold", "EternaFold", "IPKnot",
          "NeuralFold", "MXFold2", "pKnots", "Simfold", "SPOT-RNA"
        #   "NUPACK", "RNAFold", "RNAStructure",
        #   "MXFold"
          ]

headers = "algo_name, datapoint_name, lenience, sequence, true_structure, prediction, sensitivity, ppv, f1\n"

leniences = [0, 1]
for m in models:
    print(f"Working {m}")
    for lenience in leniences:
        fname = f"{m}_predictions_{lenience}_lenience.txt"
        with open(f"{base_dir}/{fname}") as fh:
            lines = fh.readlines()

        if lines[0].startswith("model") or lines[0].startswith("algo"):
            lines.pop(0)

        fstring = headers
        for line in lines:
            line = line.split(", ")
            model = line[0]
            dp = line[1]
            seq = line[2]
            real_stc = line[3]
            real_stc = CanonicalBasePairScorer.transform_structure(real_stc, seq)
            pred_stc = line[4]
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
