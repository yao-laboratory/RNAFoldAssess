import json

from rna_secstruct import SecStruct


def get_sec_struct_object(seq, stc):
    try:
        return SecStruct(seq, stc)
    except:
        return False

base_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions"
dp_file_path = f"{base_dir}/all_bprna_datapoints.txt"

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


with open(dp_file_path) as fh:
    datapoints = [line.split(", ") for line in fh.readlines()]


prediction_path = f"{base_dir}/bprna_matched_set_0.txt"
with open(prediction_path) as fh:
    predictions = [line.split(", ") for line in fh.readlines()]

print("Building datapoint->prediction map")
dp_pred_map = {}
for p in predictions:
    model = p[0]
    datapoint_name = p[1]
    pred = p[5]
    try:
        dp_pred_map[datapoint_name][model] = pred
    except KeyError:
        dp_pred_map[datapoint_name] = {model: pred}

dp_motif_data = {}
print("Building datapoint->motif map")
for dp in datapoints:
    dp_name = dp[0]
    seq = dp[1]
    stc = dp[2].strip()
    dp_motif_data[dp_name] = {
        "sequence": seq,
        "structure": stc,
        "motifs": {},
        "prediction_data": {}
    }

    motif_data = get_sec_struct_object(seq, stc)
    if not motif_data:
        continue

    for k, v in motif_data.motifs.items():
        if len(v.sequence) <= 10:
            # Skip short sequence motifs
            continue

        key = v.m_type + "_" + v.sequence + "_" + v.structure
        positions = v.positions

        dp_motif_data[dp_name]["motifs"][key] = {"positions": positions}


    dp_predictions = dp_pred_map[dp_name]
    for m in models:
        pred = dp_predictions[m]
        dp_motif_data[dp_name]["prediction_data"][m] = {"prediction": pred, "motifs": []}
        pred_motif_data = get_sec_struct_object(seq, pred)
        if not pred_motif_data:
            continue

        predicted_motifs = []
        for k, v in pred_motif_data.motifs.items():
            if len(v.sequence) <= 10:
                # Skip short sequence motifs
                continue

            key = v.m_type + "_" + v.sequence + "_" + v.structure
            predicted_motifs.append(key)

            dp_motif_data[dp_name]["prediction_data"][m]["motifs"].append([key, v.positions])

        real_motifs = dp_motif_data[dp_name]["motifs"].keys()
        for rm in real_motifs:
            if rm not in predicted_motifs:
                rm_key = dp_motif_data[dp_name]["motifs"][rm]
                wrong_prediction = "".join([pred[i] for i in dp_motif_data[dp_name]["motifs"][rm]["positions"]])
                dp_motif_data[dp_name]["motifs"][rm][m] = {"success": False, "prediction": wrong_prediction}
            else:
                dp_motif_data[dp_name]["motifs"][rm][m] = {"success": True}


with open(f"{base_dir}/bprna_motif_prediction_data.json", "w") as fh:
    json.dump(dp_motif_data, fh)

print(f"Successfully wrote to {base_dir}/bprna_motif_prediction_data.json")
