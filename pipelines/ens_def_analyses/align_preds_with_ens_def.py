import os


ens_def_file_path = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/chem_map_ens_mfe.txt"
all_chem_map = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions/chemical_mapping_master_file.txt"

ed_map = {}

with open(ens_def_file_path) as fh:
    lines = [line.strip().split(", ") for line in fh.readlines()]

lines.pop(0)

for line in lines:
    dp = line[0]
    ens_def = line[1]
    mfe = line[2]
    ed_map[dp] = {
        "ensemble_defect": ens_def,
        "mfe": mfe
    }

headers = "dataset, model, datapoint_name, sequence, prediction, accuracy, ensemble_defect, mfe\n"

with open(all_chem_map) as fh:
    all_pred_lines = [line.strip().split(", ") for line in fh.readlines()]

print("Going through the lines")
dest_file = open("/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions/chem_map_master_ensd_mfe.txt", "w")
dest_file.write(headers)

for apl in all_pred_lines:
    dp_name = apl[2]
    data = ed_map[dp_name]
    ensemble_defect = data["ensemble_defect"]
    mfe = data["mfe"]
    line = ", ".join(line)
    line += f"{ensemble_defect}, {mfe}\n"
    dest_file.write(line)

dest_file.close()
print("Done")
