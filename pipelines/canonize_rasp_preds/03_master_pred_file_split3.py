import os

from RNAFoldAssess.models import DataPoint
from RNAFoldAssess.models.scorers import *


quartile = 3

def make_canonical(stc, seq):
    seq = seq.replace("T", "U")
    stc = list(stc)
    for i in range(len(stc)):
        nt = stc[i]
        if nt in "().":
            stc[i] = nt
        elif nt == "<":
            stc[i] = "("
        elif nt == ">":
            stc[i] = ")"
        else:
            stc[i] = "."
    stc = "".join(stc)
    stc = CanonicalBasePairScorer.transform_structure(stc, seq)
    return stc


base_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/rasp_data"
species_pred_map = {
    "ara-tha": f"{base_dir}/ara-tha/canonical",
    # "covid": f"{base_dir}/covid",
    # "ecoli": f"{base_dir}/ecoli",
    # "HIV": f"{base_dir}/HIV",
    # "human": f"{base_dir}/human/fixed_files"
}

models = ["ContextFold", "ContraFold", "EternaFold", "IPKnot",
          "NeuralFold", "NUPACK", "RNAFold",
          "RNAStructure", "pKnots", "Simfold",
          "MXFold", "MXFold2", "SPOT-RNA"]


data = []
for species, pred_base_dir in species_pred_map.items():
    print(f"Working {species}")
    for m in models:
        if species == "ara-tha":
            prefix = pred_base_dir
            pred_files = [f"{prefix}/{f}" for f in os.listdir(prefix) if "predictions" in f]
        elif species == "covid":
            if m not in ["MXFold2", "NeuralFold", "pKnots", "RNAStructure", "Simfold", "SPOT-RNA"]:
                prefix = f"{pred_base_dir}/{m}/filtered"
                pred_files = [f"{prefix}/{f}" for f in os.listdir(prefix) if "predictions" in f]
            else:
                prefix = f"{pred_base_dir}/{m}"
                pred_files = [f"{prefix}/{f}" for f in os.listdir(prefix) if "predictions" in f]
        elif species == "ecoli":
            if m not in ["MXFold2", "NeuralFold", "NUPACK", "pKnots", "RNAStructure", "Simfold", "SPOT-RNA"]:
                prefix = f"{pred_base_dir}/{m}/filtered"
                pred_files = [f"{prefix}/{f}" for f in os.listdir(prefix) if "predictions" in f]
            else:
                prefix = f"{pred_base_dir}/{m}"
                pred_files = [f"{prefix}/{f}" for f in os.listdir(prefix) if "predictions" in f]
        elif species == "HIV":
            if m not in ["ContextFold", "MXFold2", "NeuralFold", "NUPACK", "pKnots", "RNAStructure", "Simfold", "SPOT-RNA"]:
                prefix = f"{pred_base_dir}/{m}/filtered"
                pred_files = [f"{prefix}/{f}" for f in os.listdir(prefix) if "predictions" in f]
            else:
                prefix = f"{pred_base_dir}/{m}"
                pred_files = [f"{prefix}/{f}" for f in os.listdir(prefix) if "predictions" in f]

        for pf in pred_files:
            with open(f"{pf}") as fh:
                lines = fh.readlines()
            if lines[0].startswith("algo"):
                lines.pop(0)

            lines = [f"{species}, {line}" for line in lines]
            data += lines

# 2,399,787
first = data[:500000]
second = data[500000:1000000]
third = data[1000000:1500000]
last = data[1500000:]

if quartile == 1:
    data = first
elif quartile == 2:
    data = second
elif quartile == 3:
    data = third
elif quartile == 4:
    data = last

# data[0]
# 'ContraFold, 3_AT3G54400.1.exon2, {sequence}, {dbn}, 0.7004608294930875, 0.21996603152636307\n'
print("Creating file")
fstring = ""
counter = 0
for d in data:
    counter += 1
    if counter % 1500 == 0:
        print(f"Working {counter} of {len(data)}")
    d = d.split(", ")
    seq = d[3]
    if len(seq) < 10:
        continue
    ds = d[0]
    model = d[1]
    dp = d[2]
    pred = d[4]
    pred = make_canonical(pred, seq)
    fstring += f"{ds}, {dp}, {model}, {seq}, {pred}\n"

destination_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/consolidated"
with open(f"{destination_dir}/RASP_ara_canonical_preds_no_score_{quartile}.txt", "w") as fh:
    fh.write(fstring)
