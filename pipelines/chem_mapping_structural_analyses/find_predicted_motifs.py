import json

from rna_secstruct import SecStruct


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

base_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions"
pred_path = f"{base_dir}/chemical_mapping_matched_set.txt"
datasets = set()

with open(pred_path) as fh:
    predictions = [line.split(", ") for line in fh.readlines()]

dp_pred_map = {}

for line in predictions:
    dataset = line[0]
    datasets.add(dataset)
    dp_name = line[2]
    dp_pred_map[dp_name] = {"dataset": dataset}
    for m in models:
        dp_pred_map[dp_name][m] = {}

for line in predictions:
    model = line[1]
    dp_name = line[2]
    seq = line[3]
    pred = line[4]
    motifs = []

    motif_data = get_sec_struct_object(seq, pred)
    if not motif_data:
        continue

    for k, v in motif_data.motifs.items():
        if len(v.sequence) <= 10:
            # Skip short sequence motifs
            continue
        key = v.m_type + "_" + v.sequence + "_" + v.structure
        positions = v.positions
        dp_pred_map[dp_name][m][key] = positions

print("Note these datasets:")
for ds in datasets:
    print(ds)


with open(f"{base_dir}/predicted_motifs_chemical_mapping.json", "w") as fh:
    json.dump(dp_pred_map, fh)
