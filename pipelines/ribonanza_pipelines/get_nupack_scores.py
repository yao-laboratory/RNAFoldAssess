import os


reports_dir = "/common/yesselmanlab/ewhiting/reports/ribonanza/with_energies"

files = os.listdir(reports_dir)
nupack_files = [f for f in files if "NUPACK" in f]
prediction_files = [f for f in nupack_files if "predictions" in f]

all_accs = []
for f in prediction_files:
    f = open(f"{reports_dir}/{f}")
    data = f.readlines()
    f.close()
    for d in data:
        d = d.split(", ")
        acc = float(d[4])
        all_accs.append(acc)

print(f"Data points: {len(all_accs)}")
avg = sum(all_accs) / len(all_accs)
print(f"Average accuracy: {round(avg, 4)}")

