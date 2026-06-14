import os, json

from rna_secstruct import SecStruct
from RNAFoldAssess.models.scorers import *


def get_sec_struct_object(seq, stc):
    try:
        return SecStruct(seq, stc)
    except:
        return False


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

matched_base = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions"
matched_human = f"{matched_base}/rasp_matched_set_human.txt"
matched_ara = f"{matched_base}/rasp_ara_matched_set.txt"
matched_microbe = f"{matched_base}/rasp_microbe_matched_set.txt"

data = []
for matched_path in [matched_human, matched_ara, matched_microbe]:
    with open(matched_path) as fh:
        data += fh.readlines()


dp_map = {}
print("Building initial map")
for d in data:
    d = d.split(", ")
    dp_name = d[1]
    if dp_name not in dp_map:
        dp_map[dp_name] = {}
        seq = d[2]
        seq = seq.upper().replace("T", "U")
        dp_map[dp_name]["sequence"] = seq
        for m in models:
            dp_map[dp_name][m] = {}


print("Extracting motifs")

for d in data:
    d = d.split(", ")
    model = d[0]
    dp_name = d[1]
    pred = d[3]
    seq = dp_map[dp_name]["sequence"]

    pred = CanonicalBasePairScorer.transform_structure(pred, seq)
    pred_motif_data = get_sec_struct_object(seq, pred)
    if not pred_motif_data:
        continue

    predicted_motifs = []
    for k, v in pred_motif_data.motifs.items():

        key = v.m_type + "_" + v.sequence + "_" + v.structure
        predicted_motifs.append(key)
        dp_map[dp_name][m][key] = v.positions

dest = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions/rasp_all_motifs.json"
with open(dest, "w") as fh:
    json.dump(dp_map, fh)

print("Done")
