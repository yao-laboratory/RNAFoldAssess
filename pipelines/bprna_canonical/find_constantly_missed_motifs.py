import json


base_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions"
json_path = f"{base_dir}/motif_prediction_by_datapoint_bprna_trimmed.json"

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

print("Loading data")
with open(json_path) as fh:
    data = json.load(fh)

print(f"Loaded {len(data)} motifs")

difficult_motifs = []
for motif, m_data in data.items():
    occurences = m_data["occurences"]
    models_missed = len(m_data["false_negative_by"])
    all_missed = int(models_missed / occurences) == len(models)
    if all_missed:
        difficult_motifs.append(motif)

print(f"found {len(difficult_motifs)} difficult motifs")

with open(f"{base_dir}/bprna_difficult_motifs.txt", "w") as fh:
    for dm in difficult_motifs:
        fh.write(f"{dm}\n")
