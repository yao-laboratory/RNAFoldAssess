lowest_quartile = 0.643

base_dir = "/common/yesselmanlab/ewhiting/reports/rnandria"

def pri_file_name(model_name):
    return f"{base_dir}/{model_name}_rnandria_pri_miRNA_predictions.txt"

def human_file_name(model_name):
    return f"{base_dir}/{model_name}_rnandria_human_mRNA_predictions.txt"

accuracies = []
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

destination_dir = "/common/yesselmanlab/ewhiting/dataset_analyses/rnandria"
good_guesses = open(f"{destination_dir}/RNAndria_good_guesses.txt", "w")
bad_guesses = open(f"{destination_dir}/RNAndria_bad_guesses.txt", "w")

for m in models:
    # Get pri miRNA predictions
    pri_path = pri_file_name(m)
    pf = open(pri_path)
    data = pf.readlines()
    pf.close()
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
    # Get human predictions
    human_path = human_file_name(m)
    hf = open(human_path)
    data = hf.readlines()
    hf.close()
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
