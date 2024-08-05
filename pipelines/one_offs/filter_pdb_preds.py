import os


# Original PDB predictions might not have been filtered via the representative set.
# Furthermore, I need to filter out ribosomes from the predictions.

whitelist_id_files = "/common/yesselmanlab/ewhiting/data/crystal_all/filtered_ids.txt"

with open(whitelist_id_files) as f:
    whitelist_ids = [d.strip() for d in f.readlines()]

report_dir = f"/mnt/nrdstor/yesselmanlab/ewhiting/reports/crystal_all"
destination_dir = f"{report_dir}/filtered_predictions"

reports = [d for d in os.listdir(report_dir) if d.endswith(".txt")]

for report in reports:
    fstring = "algo_name, datapoint_name, lenience, sequence, true_structure, prediction, sensitivity, ppv, f1\n"
    with open(f"{report_dir}/{report}") as f:
        data = f.readlines()[1:] # Remove the header
    for d in data:
        spl = d.split(", ")
        datapoint = spl[1]
        pdb_id = datapoint[:4]
        if pdb_id in whitelist_ids:
            fstring += d
    with open(f"{destination_dir}/{report}", "w") as new_report:
        new_report.write(fstring)
