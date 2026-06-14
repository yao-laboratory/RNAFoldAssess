import json


base_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions"

print("opening file")
with open(f'{base_dir}/chem_map_preds_and_scores.json') as fh:
    data = json.load(fh)

dbn_str = ""

print("Collecting DBNs")
for dp, items in data.items():
    model_preds = items["preds"]
    for _model, pred_data in model_preds.items():
        if "prediction" in pred_data:
            dbn_str += pred_data["prediction"]


isolated_dbn_symbols = set(dbn_str)
print(isolated_dbn_symbols)
