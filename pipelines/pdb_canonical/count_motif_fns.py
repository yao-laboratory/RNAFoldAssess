import json


base_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions"
json_path = f"{base_dir}/pdb_motif_prediction_data_trimmed.json"

models = [
    "ContextFold",
    "ContraFold",
    "EternaFold",
    "IPKnot",
    "MXFold",
    "MXFold2",
    "Neuralfold",
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

print(f"Loaded {len(data):,} datapoints\n")

"""
Each datum has these keys: sequence, structure, motifs, prediction_data

motifs:
    Dictionary where each key is a motif key, e.g., HELIX_GUGAUC&GGUUGC_((((((&))))))
    Each value has positions and prediction data for each model. For example:

    ```
    k = "bpRNA_RFAM_1814"
    motif = "HELIX_GUGAUC&GGUUGC_((((((&))))))"
    motif_data = data[k]["motifs"][motif]
    motif_data["ContextFold"]
    # => {"success": False, "prediction": "(((((())))))"}
    ```

    Note that the "prediction" is the model's prediction of the datapoint at the
    positions of the motif (as defined by rna_sec_struct). The "success" value is
    False if rna_sec_struct determines that the motif in question (assigned to the
    `motif` variable above) is not present in the list of motifs in the model's
    secondary structure prediction.

prediction_data:
    Dictionary containing data about each model's prediction for a particular
    datapoint. The dictionary for each model contains a prediction and list of
    motifs in that prediction. The "motifs" key is a two-dimensional list, each
    item is is a two-item list where the first item is a motif-key and the second
    item is a list of positions. Consider the example:

    ```
    k = "bpRNA_RFAM_1814"
    model = "ContextFold"
    data[k]["prediction_data"][model]
    ###
    {
        'prediction': '(((((((.(((((.......(((.((((((.....)))))).)))))))).....))))))).',
        'motifs': [
            ['HELIX_AGUGAUC&GGUUGCU_(((((((&)))))))', [0, 1, 2, 3, 4, 5, 6, 55, 56, 57, 58, 59, 60, 61]],
            ['JUNCTION_CUA&UUGGUCG_(.(&).....)', [6, 7, 8, 49, 50, 51, 52, 53, 54, 55]],
            ['HELIX_AGGUU&GGCUU_(((((&)))))', [8, 9, 10, 11, 12, 45, 46, 47, 48, 49]],
            ['JUNCTION_UAUUUUGGA&UG_(.......(&))', [12, 13, 14, 15, 16, 17, 18, 19, 20, 44, 45]],
            ['HELIX_UCUGUU&AACAGG_((((((&))))))', [24, 25, 26, 27, 28, 29, 35, 36, 37, 38, 39, 40]]
        ]
    }
    ###
    ```
"""

all_bps = list(data.keys())
all_motifs = set()

print("Building unique set of motifs")
for dp, dp_data in data.items():
    motifs = dp_data["motifs"].keys()
    for m in motifs:
        all_motifs.add(m)

print(f"Found {len(all_motifs):,} unique motifs\n")

motif_data = {}
for m in all_motifs:
    motif_data[m] = {
        "occurences": 0,
        "false_negative_by": [],
        "found_in_datapoints": []
    }

print("Finding all false negatives ...\n")
for dp, dp_data in data.items():
    motifs = dp_data["motifs"]
    for motif, model_preds in motifs.items():
        motif_data[motif]["occurences"] += 1
        motif_data[motif]["found_in_datapoints"].append(dp)
        for m in models:
            try:
                if not model_preds[m]["success"]:
                    motif_data[motif]["false_negative_by"].append(m)
            except KeyError as ex:
                backup_motif_data = data[dp]["prediction_data"][m]["motifs"]
                if motif not in backup_motif_data:
                    motif_data[motif]["false_negative_by"].append(m)

print("Writing file")
with open(f"{base_dir}/motif_prediction_by_datapoint_pdb_trimmed.json", "w") as fh:
    json.dump(motif_data, fh)

print("Done\n")
