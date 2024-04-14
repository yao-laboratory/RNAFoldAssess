import os

from RNAFoldAssess.utils.secondary_structure_tools import SecondaryStructureTools


dataset = "ribonanza"
report_home = f"/common/yesselmanlab/ewhiting/reports/{dataset}"
destination_dir = f"/common/yesselmanlab/ewhiting/reports/{dataset}/with_energies"


prediction_files = [f for f in os.listdir(report_home) if f.endswith("predictions.txt")]

model_names = set()
file_prefixes = set()

for pf in prediction_files:
    model_name = pf.split("_")[0]
    model_names.add(model_name)
    file_prefix = pf.split("_predictions.txt")[0]
    file_prefixes.add(file_prefix)

rw_files = []
for fp in file_prefixes:
    read_file = f"{report_home}/{fp}_predictions.txt"
    write_file = f"{destination_dir}/{fp}_predictions_with_energies.txt"
    rw_files.append([
        read_file, write_file
    ])

# for i in rw_files:
#     print(i)

print("Starting read/write loop")
for rf, wf in rw_files:
    rf = open(rf)
    data = rf.readlines()
    rf.close()
    wf = open(wf, "w")
    for d in data:
        items = d.split(", ")
        seq = items[2]
        stc = items[3]
        fe = SecondaryStructureTools.get_free_energy(seq, stc)
        d = d.strip()
        d += f", {fe}\n"
        wf.write(d)
    wf.close()
