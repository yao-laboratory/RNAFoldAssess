import os


prediction_dirs = "/work/yesselmanlab/ewhiting/spot_scripts/bprna"

empty_dirs = []

for i in range(103):
    files = os.listdir(f"{prediction_dirs}/part_{i}")
    if len(files) == 0:
        empty_dirs.append(f"part_{i}")


with open(f"{prediction_dirs}/empty_dirs.txt", "w") as fh:
    for d in empty_dirs:
        fh.write(f"{d.split('_')[1]}\n")

print(f"Found {len(empty_dirs)} empty directories")
