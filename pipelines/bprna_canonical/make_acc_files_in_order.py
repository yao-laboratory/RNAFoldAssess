import os


base_dir = "/work/yesselmanlab/ewhiting/bprna_canonical_reports"
dest_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions"

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

# Put all predictions into master file
# for lenience in [0, 1]:
#     report_file = open(f"{dest_dir}/bprna_master_file_{lenience}.txt", "w")
#     for m in models:
#         fpath = f"{base_dir}/{m}_master_{lenience}_lenience.txt"
#         with open(fpath) as fh:
#             preds = fh.readlines()

#         if preds[0].startswith("model_name"):
#             preds.pop(0)

#         for p in preds:
#             report_file.write(p)

#     report_file.close()


# Match predictions
model_index = 0
dp_name_index = 1
seq_index = 3
real_stc_index = 4
pred_stc_index = 5
sen_index = 6
ppv_index = 7
f1_index = 8

def clean_structure(stc):
    stc = list(stc)
    for i in range(len(stc)):
        if stc[i] not in "().":
            stc[i] = "."

    stc = "".join(stc)
    return stc

def build_dp_map(preds):
    datapoint_map = {}
    for p in preds:
        dp = p[dp_name_index]
        real_stc = clean_structure(p[real_stc_index])
        datapoint_map[dp] = {
            "sequence": p[seq_index].upper(),
            "structure": real_stc,
            "models": {}
        }

    for p in preds:
        dp = p[dp_name_index]
        model = p[model_index]
        pred_stc = clean_structure(p[pred_stc_index])
        sen = float(p[sen_index].strip())
        ppv = float(p[ppv_index].strip())
        f1 = float(p[f1_index].strip())

        model_info = {"sensitivity": sen, "ppv": ppv, "f1": f1, "prediction": pred_stc}
        datapoint_map[dp]["models"][model] = model_info

    return datapoint_map


for lenience in [0, 1]:
    print(f"Working on {lenience} lenience predictions")
    datapoints = {}
    with open(f"{dest_dir}/bprna_master_file_{lenience}.txt") as fh:
        predictions = [line.split(", ") for line in fh.readlines()]
        print(f"\tBuilding datapoint map from {len(predictions)} predictions")
        dp_map = build_dp_map(predictions)

    matched_dps = {}
    print(f"\tBuilding matched datapoint map")
    for dp, dp_data in dp_map.items():
        model_info = dp_data["models"]
        if len(model_info) == len(models):
            matched_dps[dp] = dp_data

    report_str = ""
    print(f"\tBuilding report string")
    counter = 0
    for dp in matched_dps:
        counter += 1
        if counter % 20000 == 0:
            print(f"\t\tWorking #{counter:,} of {len(matched_dps)}")
        for m in models:
            line = f"{m}, {dp}, {lenience}, "
            seq = matched_dps[dp]["sequence"]
            stc = matched_dps[dp]["structure"]
            pred = matched_dps[dp]["models"][m]["prediction"]
            line += f"{seq}, {stc}, {pred}, "
            sens = matched_dps[dp]["models"][m]["sensitivity"]
            ppv = matched_dps[dp]["models"][m]["ppv"]
            f1 = matched_dps[dp]["models"][m]["f1"]
            line += f"{str(sens)}, {str(ppv)}, {str(f1)}\n"
            report_str += line

    with open(f"{dest_dir}/bprna_matched_set_{lenience}.txt", "w") as fh:
        fh.write(report_str)

print("Done!")
