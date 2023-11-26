import os, datetime

from RNAFoldAssess.models import DataPointFromCrystal
from RNAFoldAssess.models.predictors import *
from RNAFoldAssess.models.scorers import *

model_name = "MXFold"
model = MXFold()
model_path = os.path.abspath("/home/yesselmanlab/ewhiting/mxfold/build/mxfold")
data_type_name = "bpRNA-1m-90"
headers = "algo_name, datapoint_name, lenience, sensitivity, ppv, F1, data_point_type"
leniences = []

dbn_path = "/common/yesselmanlab/ewhiting/data/bprna/dbnFiles"
files = os.listdir(dbn_path)
file_len = len(files)

analysis_report_path = f"/common/yesselmanlab/ewhiting/reports/{model_name}_{data_type_name}_report.txt"
pipeline_report_path = f"/common/yesselmanlab/ewhiting/reports/{model_name}_{data_type_name}.txt"

counter = 0
skipped = 0

def sequence_to_file(name, sequence):
    # To seq file
    name = name.replace(" ", "_")
    name = name.replace("/", "")
    name = name.replace("'", "")
    name = name.replace("(", "")
    name = name.replace(")", "")
    name = name.replace("[", "")
    name = name.replace("]", "")
    name = name.replace("{", "")
    name = name.replace("}", "")
    name = name.replace("<", "")
    name = name.replace(">", "")
    name = name.replace(";", "")
    name = name.replace(",", "")
    name = name.replace("|", "")
    name = name.replace("`", "")
    name = name.replace('"', "")
    name = name.replace("$", "S")
    name = name.replace("&", "and")
    name = name.replace("~", "")
    if len(name) > 200:
        name = name[0:200]
    f = open(f"{name}.seq", "w")
    f.write(sequence)
    f.close()
    path = os.path.abspath(f"{name}.seq")
    return path

lengths = []
sensitivities = {}
ppvs = {}
f1s = {}
lowest_sensitivity = {}
lowest_ppv = {}
lowest_f1 = {}
leniences = [0, 1]
for lenience in leniences:
    sensitivities[f"{lenience}"] = []
    ppvs[f"{lenience}"] = []
    f1s[f"{lenience}"] = []
    lowest_sensitivity[f"{lenience}"] = [1.0, ""]
    lowest_ppv[f"{lenience}"] = [1.0, ""]
    lowest_f1[f"{lenience}"] = [1.0, ""]


f = open(analysis_report_path, "w")
f.write(f"{headers}\n")

print(f"Starting analysis on {file_len} files ...")
for file in files:
    if counter % 125 == 0:
        print(f"Completed {counter} files")
    dbn_file = open(f"{dbn_path}/{file}")
    data = dbn_file.readlines()
    dbn_file.close()
    if len(data) != 5:
        print(f"Skipping {file} for weird file format")
        skipped += 1
    name = data[0].split("#Name: ")[1].strip()
    data_type = name.split("_")[1]
    sequence = data[3].strip()
    true_structure = data[4].strip()
    input_file_path = sequence_to_file(name, sequence)
    try:
        model.execute(model_path, input_file_path)
        prediction = model.get_ss_prediction()
        for lenience in leniences:
            f.write(f"{model_name}, {name}, {lenience}, ")
            scorer = BasePairScorer(true_structure, prediction, lenience)
            scorer.evaluate()
            s = scorer.sensitivity
            p = scorer.ppv
            f1 = scorer.f1
            sensitivities[f"{lenience}"].append(s)
            ppvs[f"{lenience}"].append(p)
            f1s[f"{lenience}"].append(f1)

            if s < lowest_sensitivity[f"{lenience}"][0]:
                lowest_sensitivity[f"{lenience}"][0] = s
                lowest_sensitivity[f"{lenience}"][1] = name

            if p < lowest_ppv[f"{lenience}"][0]:
                lowest_ppv[f"{lenience}"][0] = p
                lowest_ppv[f"{lenience}"][1] = name

            if f1 < lowest_f1[f"{lenience}"][0]:
                lowest_f1[f"{lenience}"][0] = f1
                lowest_f1[f"{lenience}"][1] = name

            f.write(f"{s}, {p}, {f1}\n")
        counter += 1
    except:
        skipped += 1
        continue

f.close()

