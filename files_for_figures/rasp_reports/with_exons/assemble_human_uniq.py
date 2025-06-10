import os


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

report_file_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/rasp_data/human/fixed_files"
figure_dest = "/home/yesselmanlab/ewhiting/RNAFoldAssess/files_for_figures/rasp_reports/with_exons/acc_files/human"

if not os.path.exists(figure_dest):
    os.mkdir(figure_dest)

dp_loc = 1
acc_loc = 4
all_models_count = len(models)

dp_score_map = {}

for f in os.listdir(report_file_dir):
    with open(f"{report_file_dir}/{f}") as fh:
        lines = fh.readlines()

    model = f.split("_")[0]
    lines = [line.split(", ") for line in lines]
    for line in lines:
        dp_name = line[dp_loc]
        score = line[acc_loc]
        try:
            dp_score_map[dp_name][model] = score
        except KeyError:
            dp_score_map[dp_name] = {model: score}


model_acc_map = {}
for m in models:
    model_acc_map[m] = []

shared = []
shared_not_spot = []

for dp, score_map in dp_score_map.items():
    models_predicted = list(score_map.keys())
    if len(models_predicted) >= all_models_count:
        print(f"{dp} predicted {len(models_predicted)} times")
        shared.append(dp)

    if "SPOT-RNA" not in models_predicted and len(models_predicted) == (all_models_count - 1):
        shared_not_spot.append(dp)

with open(f"{figure_dest}/rasp_human_shared.txt", "w") as fh:
    fh.write("\n".join(shared))

with open(f"{figure_dest}/rasp_human_shared_no_spot.txt", "w") as fh:
    fh.write("\n".join(shared_not_spot))
