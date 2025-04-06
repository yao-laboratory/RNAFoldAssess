import json


base_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions"
json_path = f"{base_dir}/motif_prediction_by_datapoint_pdb_trimmed.json"
motif_list_path = f"{base_dir}/pdb_difficult_motifs.txt"

with open(motif_list_path) as fh:
    interesting_motifs = [line.strip() for line in fh.readlines()]

with open(json_path) as fh:
    json_data = json.load(fh)

datapoint_fstring = ""
fstring = ""

for motif in interesting_motifs:
    pred_data = json_data[motif]
    dps = pred_data["found_in_datapoints"]
    for dp in dps:
        fstring += f"{dp} has a {motif} that is never detected\n"
        datapoint_fstring += f"{dp}\n"


with open(f"{base_dir}/pdb_missed_motifs.txt", "w") as fh:
    fh.write(fstring)

with open(f"{base_dir}/datapoints_in_pdb_missed_motifs.txt", "w") as fh:
    fh.write(datapoint_fstring)
