import os, json

from rna_secstruct import SecStruct


def get_sec_struct_object(seq, stc):
    try:
        return SecStruct(seq, stc)
    except:
        return False

base_report_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/rasp_data"
species = "human"
report_dir = f"{base_report_dir}/{species}/fixed_files"
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

matched_path = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions/rasp_matched_set_human.txt"
with open(matched_path) as fh:
    data = fh.readlines()


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
    pred_motif_data = get_sec_struct_object(seq, pred)
    if not pred_motif_data:
        continue

    predicted_motifs = []
    for k, v in pred_motif_data.motifs.items():

        key = v.m_type + "_" + v.sequence + "_" + v.structure
        predicted_motifs.append(key)
        dp_map[dp_name][m][key] = v.positions

dest = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions/rasp_human_motif_preds.json"
with open(dest, "w") as fh:
    json.dump(dp_map, fh)

print("Done")
