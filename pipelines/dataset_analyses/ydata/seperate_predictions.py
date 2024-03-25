lowest_quartile = 0.8778

base_dir = "/common/yesselmanlab/ewhiting/reports/ydata"

def file_name(model_name):
    return f"{base_dir}/{model_name}_YesselmanDMS_report.txt"


accuracies = []
models = [
    "ContextFold",
    "ContraFold",
    "EternaFold",
    "IPknot",
    "MXFold",
    "RandomPredictor",
    "RNAFold",
    "SeqFold"
]

destination_dir = "/common/yesselmanlab/ewhiting/dataset_analyses/ydata"
good_guesses = open(f"{destination_dir}/ydata_good_guesses.txt", "w")
bad_guesses = open(f"{destination_dir}/ydata_bad_guesses.txt", "w")

for m in models:
    path = file_name(m)
    f = open(path)
    data = f.readlines()
    f.close()
    # Get rid of headers
    if data == []:
        continue
    data.pop(0)
    for d in data:
        acc = float(d.split(", ")[4])
        if acc <= lowest_quartile:
          bad_guesses.write(d)
        else:
          good_guesses.write(d)

bad_guesses.close()
good_guesses.close()
