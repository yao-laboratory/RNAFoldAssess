import os


dest_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions"

rasp_folders = [
    "covid",
    "ecoli",
    "HIV"
]

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

base_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/rasp_data"

def get_prediction_files(model_name, species):
    if model_name in ["NeuralFold", "NUPACK", "RNAStructure", "pKnots", "Simfold", "MXFold2", "SPOT-RNA"]:
        predictions_dir = f"{base_dir}/{species}/{model_name}"
    else:
        predictions_dir = f"{base_dir}/{species}/{model_name}/filtered/with_energies"
    all_files = os.listdir(predictions_dir)
    files = [f"{predictions_dir}/{f}" for f in all_files if f.endswith("predictions.txt")]
    return files

print("Getting accuracies")
all_lines = []
for folder in rasp_folders:
    for m in models:
        print(m)
        files = get_prediction_files(m, folder)
        for f in files:
            print(f"\t- {f}")
            with open(f) as fh:
                data = fh.readlines()
            if data == []:
                continue
            # Get rid of header
            if data[0].startswith("algo"):
                data.pop(0)
            all_lines += data


with open(f"{dest_dir}/rasp_microbe_predictions.txt", "w") as fh:
    fh.write("".join(all_lines))

print("Done")
