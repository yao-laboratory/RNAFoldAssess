import os, json


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

# with open(pred_path) as fh:
#     predictions = [line.split(", ") for line in fh.readlines()]


# def pred_report(model, predictions):
#     print(f"{model} --")
#     all_pred_len = len(predictions)
#     print(f"\t{all_pred_len} predictions")
#     uniq_preds = set(predictions)
#     uniq_pred_len = len(uniq_preds)
#     diff = all_pred_len - uniq_pred_len
#     if diff != 0:
#         print(f"\tdiscrepancy of {diff}")
    
# model_dp_map = {}
# for m in models:
#     model_dp_map[m] = []

# for line in predictions:
#     model = line[1]
#     dp_name = line[2]
#     model_dp_map[model].append(dp_name)

# for m, preds in model_dp_map.items():
#     pred_report(m, preds)

# ^^ No discrepancies
print("Loading motif json")

with open(f"{base_dir}/predicted_motifs_chemical_mapping.json") as fh:
    data = json.load(fh)

all_dps = list(data.keys())
uniq_dps = set(all_dps)

print(f"There are {len(all_dps)} datapoints in the dictionary")
diff = len(all_dps) - len(uniq_dps)
print(f"There are {diff} discrepencies")
