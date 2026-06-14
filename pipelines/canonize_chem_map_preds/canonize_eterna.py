import os


from RNAFoldAssess.models import CanonicalBasePairScorer, EternaDataPoint
from RNAFoldAssess.models import DSCIException, DSCITypeError, DSCIValueError


dp_path = "/mnt/nrdstor/yesselmanlab/ewhiting/data/translated_eterna_data/eterna.json"
report_path = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/eterna_data/with_energy"
dest_dir = f"{report_path}/canonical"

datapoints = EternaDataPoint.factory(dp_path)

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

def remove_pseudoknots(stc):
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
    return stc

for m in models:
    print(f"Working {m}")
    files = [f for f in os.listdir(report_path) if f"{m}_" in f]
    data = []
    for f in files:
        with open(f"{report_path}/{f}") as fh:
            lines = fh.readlines()

        if lines[0].startswith("algo"):
            lines.pop(0)

        data += lines

    data = [line.split(', ') for line in data]

    dp_seq = {}
    for d in data:
        dp_name = d[1]
        seq = d[2]
        non_canonical_structure = d[3]
        non_canonical_structure = remove_pseudoknots(non_canonical_structure)
        canonical_structure = CanonicalBasePairScorer.transform_structure(non_canonical_structure, seq)
        dp_seq[dp_name] = canonical_structure

    fstring = ""
    for dp in datapoints:
        try:
            stc = dp_seq[dp.name]
            score = dp.assess_prediction(stc)
            acc = score["accuracy"]
            p = score["p"]
            line = f"{m}, {dp.name}, {dp.sequence}, {stc}, {acc}, {p}\n"
            fstring += line
        except KeyError:
            print(f"KeyError: {m}, {dp.name}")
            continue

    with open(f"{dest_dir}/{m}_canonical_predictions.txt", "w") as fh:
        fh.write(fstring)


print("Done")
