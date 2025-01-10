def parse_structure(structure):
    # structure exampe: "..((((...))))..((..))."
    bps = []
    for i1, c1 in enumerate(structure):
        if c1 != '(':
            continue
        count = 1
        for i2, c2 in enumerate(structure[i1 + 1:]):
            if c2 == '(':
                count += 1
            elif c2 == ')':
                count -= 1
                if count == 0:
                    bps.append((i1, i1 + i2 + 1))
                    break
    return bps


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

model_gu = {}
for m in models:
    model_gu[m] = False

all_bprna_preds = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions/bprna_master_file_0.txt"
with open(all_bprna_preds) as fh:
    data = fh.readlines()

data = [d.split(", ") for d in data]

WOBBLE_PAIRS = ["UG", "GU"]

model_index = 0
seq_index = 3
pred_index = 5

for d in data:
    model = d[model_index]
    seq = d[seq_index]
    pred = d[pred_index]
    base_pair_coordinates = parse_structure(pred)
    base_pair_nts = [f"{seq[i]}{seq[j]}" for i, j in base_pair_coordinates]
    for bp in base_pair_nts:
        if bp in WOBBLE_PAIRS:
            model_gu[model] = True
            break


for m, can_predict_wobble in model_gu.items():
    if can_predict_wobble:
        print(f"{m} can make Wobble predictions")
    else:
        print(f"{m} has NOT made Wobble predictions in bprna set")

# Output
# ContextFold can make Wobble predictions
# ContraFold can make Wobble predictions
# EternaFold can make Wobble predictions
# IPKnot can make Wobble predictions
# MXFold can make Wobble predictions
# MXFold2 can make Wobble predictions
# NeuralFold can make Wobble predictions
# NUPACK can make Wobble predictions
# pKnots can make Wobble predictions
# RNAFold can make Wobble predictions
# RNAStructure can make Wobble predictions
# Simfold can make Wobble predictions
# SPOT-RNA can make Wobble predictions

