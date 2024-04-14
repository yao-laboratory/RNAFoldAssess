import os

from RNAFoldAssess.utils.secondary_structure_tools import SecondaryStructureTools


report_dir = "/common/yesselmanlab/ewhiting/reports/eterna_data"
destination_dir = "/common/yesselmanlab/ewhiting/reports/eterna_data/with_energy"
files = os.listdir(report_dir)
files = [f for f in files if f.endswith("pipeline_report.txt")]



for file in files:
    dest_file = open(f"{destination_dir}/{file}", "w")
    f = open(f"{report_dir}/{file}")
    data = f.readlines()
    f.close()
    data.pop(0)
    print(f"Starting on {f}")
    counter = 0
    len_data = len(data)
    for d in data:
        if counter % 200 == 0:
            print(f"Finished {counter} of {len_data}")
        d = d.strip()
        items = d.split(", ")
        seq = items[2]
        stc = items[3]
        fe = SecondaryStructureTools.get_free_energy(seq, stc)
        d += f", {fe}\n"
        dest_file.write(d)
        counter += 1
    dest_file.close()

