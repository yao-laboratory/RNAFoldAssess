import os


base_dir = "/common/yesselmanlab/ewhiting/reports/eterna_data/ranked"
bad_file = open(f"{base_dir}/EternaData_bad_predictions.txt")
mid_file = open(f"{base_dir}/EternaData_mid_predictions.txt")
good_file = open(f"{base_dir}/EternaData_good_predictions.txt")


models = [
    "ContextFold",
    "ContraFold",
    "EternaFold",
    "IPKnot",
    "MXFold",
    "RandomPredictor",
    "RNAFold",
    "SeqFold"
]

bad_models = {}
mid_models = {}
good_models = {}

bad_data = bad_file.read()
mid_data = mid_file.read()
good_data = good_file.read()

bad_file.close()
mid_file.close()
good_file.close()

for m in models:
    bad_models[m] = bad_data.count(m)
    mid_models[m] = mid_data.count(m)
    good_models[m] = good_data.count(m)


f = open("model_performance.txt", "w")
for m in models:
    line = f"{m}\t{bad_models[m]}\t{mid_models[m]}\t{good_models[m]}\n"
    f.write(line)

f.close()
