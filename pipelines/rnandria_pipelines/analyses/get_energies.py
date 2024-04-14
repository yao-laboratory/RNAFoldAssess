import os


from RNAFoldAssess.utils.secondary_structure_tools import SecondaryStructureTools

base_dir = "/common/yesselmanlab/ewhiting/reports/rnandria"
destination_dir = "/common/yesselmanlab/ewhiting/reports/rnandria/with_energies"

files = [f for f in os.listdir(base_dir) if f.endswith("predictions.txt")]


for file in files:
    print(f"Working file {file}")
    f = open(f"{base_dir}/{file}")
    data = f.readlines()
    counter = 0
    len_data = len(data)
    dest_file = open(f"{destination_dir}/{file}", "w")
    for d in data:
        if counter % 200 == 0:
            print(f"Working {counter} of {len_data}")
        d = d.strip()
        items = d.split(", ")
        seq = items[2]
        stc = items[3]
        fe = SecondaryStructureTools.get_free_energy(seq, stc)
        d += f", {fe}\n"
        dest_file.write(d)
        counter += 1
    dest_file.close()

