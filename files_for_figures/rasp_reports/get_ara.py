import os


base_path = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/rasp_data/ara-tha"

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

datapoints = []
dp_acc_map = {}
for m in models:
    dp_acc_map[m] = {}


for m in models:
    pred_files = [f for f in os.listdir(base_path) if f"{m}_" in f]
    all_accs = []
    if len(pred_files) == 0:
        print(f"Need to generate preds for {m}")
    for pf in pred_files:
        with open(f"{base_path}/{pf}") as fh:
            pred_data = fh.readlines()

        if pred_data[0].startswith("algo"):
            pred_data.pop(0)

        pred_data = [pd.split(", ") for pd in pred_data]
        dps = [pd[1] for pd in pred_data]
        datapoints += dps

datapoints = set(datapoints)
datapoints = list(datapoints)
datapoints.sort()
print(f"Found {len(datapoints)} unique datapoints")


# for m in models:
#     pred_files = [f for f in os.listdir(base_path) if f"{m}_" in f]
#     all_accs = []
#     if len(pred_files) == 0:
#         print(f"Need to generate preds for {m}")
#     for pf in pred_files:
#         with open(f"{base_path}/{pf}") as fh:
#             pred_data = fh.readlines()

#         if pred_data[0].startswith("algo"):
#             pred_data.pop(0)

#         pred_data = [pd.split(", ") for pd in pred_data]
#         accs = [pd[4] for pd in pred_data]

