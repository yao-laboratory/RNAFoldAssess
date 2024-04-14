lowest_quartile = 0.643
highest_quartile = 0.743

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
mid_guesses = open(f"{destination_dir}/RNAndria_mid_guesses.txt", "w")
bad_guesses = open(f"{destination_dir}/RNAndria_bad_guesses.txt", "w")

model_perf = {}
for m in models:
    model_perf[m] = {"low": 0, "mid": 0, "high": 0}

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
          model_perf[m]["low"] += 1
        elif acc >= highest_quartile:
          good_guesses.write(d)
          model_perf[m]["high"] += 1
        else:
            mid_guesses.write(d)
            model_perf[m]["mid"] += 1
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
mid_guesses.close()
good_guesses.close()

f = open("model_performance.txt", "w")

line = "modle, low, high, middle\n"
for m in model_perf:
    low = model_perf[m]["low"]
    mid = model_perf[m]["mid"]
    hi = model_perf[m]["high"]
    line += f"{m}\t{low}\t{hi}\t{mid}\n"

f.write(line)
