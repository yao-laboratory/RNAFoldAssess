import os


from RNAFoldAssess.utils.secondary_structure_tools import SecondaryStructureTools


base_dir = "/common/yesselmanlab/ewhiting/reports/bprna"
destination_dir = f"{base_dir}/filtered"
reference = sorted(set("ACGU"))

files = os.listdir(base_dir)
files = [f for f in files if f.endswith("report.txt")]

for ff in files:
    print(f"Working {ff}")
    f = open(f"{base_dir}/{ff}")
    data = f.readlines()
    f.close()
    f = open(f"{destination_dir}/{ff}", "w")
    for i, d in enumerate(data):
        d = d.strip()
        items = d.split(", ")
        seq = items[3]
        stc = items[4]
        alphabet = set(seq)
        for s in seq:
            if seq not in reference:
                break
        stc = stc.replace("[", ".").replace("]", ".")
        if i % 2 == 0:
            # Doing this because every two lines is the same prediction
            fe = SecondaryStructureTools.get_free_energy(seq, stc)
        d += f", {fe}\n"
        f.write(d)
    f.close()