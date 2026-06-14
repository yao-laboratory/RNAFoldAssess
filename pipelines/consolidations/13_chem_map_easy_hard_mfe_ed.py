# Go to /mnt/nrdstor/yesselmanlab/ewhiting/vienna
# and run
# module load viennarna

import vienna


base_path = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions"
file_map = {
    "easy": f"{base_path}/chem_map_easy_master.csv",
    "hard": f"{base_path}/chem_map_hard_master.csv"
}

for difficulty, f_loc in file_map.items():
    print(f"Working {difficulty} cases")
    new_f_locat = f_loc.replace("_master.csv", "_mfe_ed_master.csv")
    new_f = open(new_f_locat, "w")
    with open(f_loc) as fh:
        data = fh.readlines()
    headers = data.pop(0).strip()
    headers += ",mfe,ens_def\n"
    new_f.write(headers)
    for d in data:
        d = d.strip()
        d = d.split(",")
        seq = d[1]
        stc_data = vienna.fold(seq)
        mfe = stc_data.mfe
        ens_def = stc_data.ens_defect
        line = ",".join(d)
        line += f",{mfe},{ens_def}\n"
        new_f.write(line)
    new_f.close()
