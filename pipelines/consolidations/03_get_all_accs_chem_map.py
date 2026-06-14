import os


chem_map_pred_map = {
    "EternaBench": "/mnt/nrdstor/yesselmanlab/ewhiting/reports/eterna_data/with_energy/canonical",
    "Ribonanza": "/mnt/nrdstor/yesselmanlab/ewhiting/reports/ribonanza/canonical",
    "RNAndria-miRNA": "/mnt/nrdstor/yesselmanlab/ewhiting/reports/rnandria/canonical",
    "RNAndria-mRNA": "/mnt/nrdstor/yesselmanlab/ewhiting/reports/rnandria/canonical",
    "YData": "/mnt/nrdstor/yesselmanlab/ewhiting/reports/ydata/canonize"
}


def get_files(ds):
    loc = chem_map_pred_map[ds]
    if ds == "RNAndria-miRNA":
        files = [f for f in os.listdir(loc) if "miRNA" in f]
    elif ds == "RNAndria-mRNA":
        files = [f for f in os.listdir(loc) if "mRNA" in f]
    else:
        files = os.listdir(loc)
    
    return files

accs = []

for ds in chem_map_pred_map.keys():
    print(f"Working {ds}")
    files = get_files(ds)
    ds_dir = chem_map_pred_map[ds]
    for f in files:
        with open(f"{ds_dir}/{f}") as fh:
            lines = fh.readlines()
        
        if lines[0].startswith("algo"):
            lines.pop(0)
        
        lines = [line.split(", ") for line in lines]
        accs += [float(line[4]) for line in lines]

print(f"Found {len(accs)} accuracies")
breakpoint()

import numpy as np

q1 = np.percentile(accs, 25)
q2 = np.percentile(accs, 50)  # This is the median
q3 = np.percentile(accs, 75)

print("Q1:", q1)
print("Median (Q2):", q2)
print("Q3:", q3)



