import os, sys

from RNAFoldAssess.models.scorers import *


base_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions"
files = ["bprna_master_file_0.txt", "bprna_master_file_1.txt"]

for f in files:
    print(f"Reading {f}")
    path = f"{base_dir}/{f}"
    new_fname = f.replace(".txt", "_canonical.txt")
    dest = f"{base_dir}/{new_fname}"
    with open(path) as fh:
        lines = fh.readlines()

    # Get rid of header
    headers = lines.pop(0)
    lines = [line.split(", ") for line in lines]

    fstring = f"{headers}"
    counter = 0
    for line in lines:
        counter += 1
        if counter % 75000 == 0 or counter >= len(lines) - 1:
            with open(f"{dest}.{counter}", "w") as fh:
                fh.write(fstring)
            fstring = f"{headers}"
            print(f"Working {counter} of {len(lines)}", file=sys.stderr)
        ds = line[0]
        model = line[1]
        lenience = line[2]
        dp = line[3]
        seq = line[4]
        new_line = f"{ds}, {model}, {lenience}, {dp}, {seq}, "
        stc = line[5]
        pred = line[6]
        stc = CanonicalBasePairScorer.transform_structure(stc, seq)
        pred = CanonicalBasePairScorer.transform_structure(pred, seq)
        new_line += f"{stc}, {pred}, "
        scorer = BasePairScorer(stc, pred, int(lenience))
        scorer.evaluate()
        sens = scorer.sensitivity
        ppv = scorer.ppv
        f1 = scorer.f1
        new_line += f"{sens}, {ppv}, {f1}\n"
        fstring += new_line

print("Done")
