import os


models = [
    "ContextFold",
    "ContraFold",
    "EternaFold",
    "RandomPredictor",
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

source_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/ribonanza/with_energies"
dest_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/ribonanza/unique_preds"

for m in models:
    pred_files = [f for f in os.listdir(source_dir) if f"{m}_" in f and "predictions" in f]
    all_data = []
    found_data = []
    for pf in pred_files:
        with open(f"{source_dir}/{pf}") as fh:
            data = fh.readlines()
        for d in data:
            dp_name = d.split(", ")[1]
            if dp_name in found_data:
                continue
            found_data.append(dp_name)
            all_data.append(d)
    print(f"{m} - Found: {len(found_data)}, All: {len(all_data)}")
    with open(f"{dest_dir}/{m}_unique_predictions.txt", "w") as fh:
        for ad in all_data:
            fh.write(ad)

print("Done")
