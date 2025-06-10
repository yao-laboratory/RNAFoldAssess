import os, json

from RNAFoldAssess.models.scorers import *


species = "human"
model_name = "pKnots"
dbn_dir = "/common/yesselmanlab/ewhiting/pknot_scripts/rasp/outputs/human/dbns"

dbn_files = os.listdir(dbn_dir)

available_dbns = [f.split(".")[0] for f in dbn_files]

base_dir = "/common/yesselmanlab/ewhiting/data/rasp_data"
json_dir = f"{base_dir}/{species}/json_files"
json_files = os.listdir(json_dir)

ch_map = {}
for jf in json_files:
    ch = jf.replace("_exons.json", "")
    with open(f"{json_dir}/{jf}") as fh:
        ch_map[ch] = json.load(fh)

    headers = "algo_name, datapoint_name, sequence, prediction, accuracy, p_value\n"

    for ch in ch_map:
        print(f"Working {ch} in {species}")
        report_file = open(f"/mnt/nrdstor/yesselmanlab/ewhiting/reports/rasp_data/{species}/{model_name}_{ch}_report.txt", "w")
        report_file.write(headers)
        data = ch_map[ch]
        counter = 0
        len_data = len(data)
        for dp in data:
            if dp["name"] not in available_dbns:
                continue
            if len(dp["sequence"]) < 10:
                continue

            pred_loc = f"{dbn_dir}/{dp['name']}.dbn"
            with open(pred_loc) as fh:
                prediction = fh.read().strip()

            if len(prediction) <= 10:
                continue

            reactivity_map = dp["reactivity_map"]
            testable_seq = ""
            testable_dbn = ""
            reactivities = [float(d[1]) for d in reactivity_map]
            for i, _reactivity in reactivity_map:
                testable_seq += dp["sequence"][i]
                testable_dbn += prediction[i]

            score = DSCI.score(
                testable_seq,
                testable_dbn,
                reactivities,
                DMS=True
            )

            accuracy = score["accuracy"]
            p = score["p"]

            line_to_write = f"{model_name}, {dp['name']}, {dp['sequence']}, {prediction}, {accuracy}, {p}\n"
            report_file.write(line_to_write)

        report_file.close()

print("Done")