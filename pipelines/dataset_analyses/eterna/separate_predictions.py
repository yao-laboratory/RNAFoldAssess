import pandas as pd


base_dir = "/common/yesselmanlab/ewhiting/reports/eterna_data/with_energy"
destination_dir = "/common/yesselmanlab/ewhiting/reports/eterna_data/ranked"

def shape_file_name(model_name):
    return f"{base_dir}/{model_name}_SHAPE_pipeline_report.txt"

def dms_file_name(model_name):
    return f"{base_dir}/{model_name}_DMS_pipeline_report.txt"

models = [
    "ContextFold",
    "ContraFold",
    "EternaFold",
    "IPKnot",
    "MXFold",
    "MXFold2",
    "RandomPredictor",
    "RNAFold",
    "SeqFold"
]


accuracies = []

for m in models:
    print(f"Working {m}")
    # Get SHAPE predictions
    shape_path = shape_file_name(m)
    sf = open(shape_path)
    data = sf.readlines()
    sf.close()
    # Get rid of headers
    data.pop(0)
    for d in data:
        items = d.strip().split(", ")
        acc = float(items[4])
        accuracies.append(acc)
    dms_path = dms_file_name(m)
    df = open(dms_path)
    data = df.readlines()
    df.close()
    # Get rid of headers
    data.pop(0)
    for d in data:
        items = d.strip().split(", ")
        acc = float(items[4])
        accuracies.append(acc)

series = pd.Series(accuracies)
print("Separating data")
stats = series.describe()

top = stats["75%"]
bottom = stats["25%"]

good_guesses = open(f"{destination_dir}/EternaData_good_predictions.txt", "w")
easily_predicted_datapoints = open(f"{destination_dir}/EternaEasyDatapoitns.txt", "w")
bad_guesses = open(f"{destination_dir}/EternaData_bad_predictions.txt", "w")
hard_datapoints = open(f"{destination_dir}/EternaHardDatapoints.txt", "w")
mid_guesses = open(f"{destination_dir}/EternaData_mid_predictions.txt", "w")

for m in models:
    print(f"Working {m}")
    # Get SHAPE predictions
    shape_path = shape_file_name(m)
    sf = open(shape_path)
    data = sf.readlines()
    sf.close()
    # Get rid of headers
    data.pop(0)
    for d in data:
        items = d.strip().split(", ")
        name = items[1]
        seq = items[2]
        acc = float(items[4])
        if acc <= bottom:
            bad_guesses.write(d)
            hard_datapoints.write(f"{name}, {seq}\n")
        elif acc >= top:
            good_guesses.write(d)
            easily_predicted_datapoints.write(f"{name}, {seq}, SHAPE\n")
        else:
            mid_guesses.write(d)
    # Get DMS predictions
    dms_path = dms_file_name(m)
    df = open(dms_path)
    data = df.readlines()
    df.close()
    for d in data:
        items = d.strip().split(", ")
        name = items[1]
        seq = items[2]
        acc = float(items[4])
        if acc <= bottom:
            bad_guesses.write(d)
            hard_datapoints.write(f"{name}, {seq}\n")
        elif acc >= top:
            good_guesses.write(d)
            easily_predicted_datapoints.write(f"{name}, {seq}, DMS\n")
        else:
            mid_guesses.write(d)

good_guesses.close()
bad_guesses.close()
mid_guesses.close()
easily_predicted_datapoints.close()
hard_datapoints.close()

print("Done")
