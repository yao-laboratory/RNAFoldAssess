import os

import pandas as pd


base_dir = "/common/yesselmanlab/ewhiting/reports/rnandria/with_energies"
destination_dir = "/common/yesselmanlab/ewhiting/reports/rnandria/analyses"
files = [f for f in os.listdir(base_dir) if f.endswith("predictions.txt")]

accuracies = []
for file in files:
    f = open(f"{base_dir}/{file}")
    data = f.readlines()
    for d in data:
        d = d.split(", ")
        acc = float(d[4])
        accuracies.append(acc)


series = pd.Series(accuracies)
stats = series.describe()
print("Writing descriptive stats")
f = open("rnandria_descriptive_stats.txt", "w")
f.write(str(stats))
f.close()

lowest = stats["25%"]
highest = stats["75%"]

top_preds = []
bottom_preds = []

accuracies = []
for file in files:
    f = open(f"{base_dir}/{file}")
    data = f.readlines()
    for d in data:
        items = d.split(", ")
        acc = float(items[4])
        if acc <= lowest:
            bottom_preds.append(d)
        elif acc >= highest:
            top_preds.append(d)

print("Writing top predicitons")
gf = open(f"{destination_dir}/top_predictions.txt", "w")
for d in top_preds:
    gf.write(d)
gf.close()

print("Writing bottom predictions")
bf = open(f"{destination_dir}/bottom_predictions.txt", "w")
for d in bottom_preds:
    bf.write(d)
bf.close()

