import os, json

from RNAFoldAssess.models.scorers import *


pred_path = "/common/yesselmanlab/ewhiting/simfold_scripts/outputs/rasp/human"
json_dir = "/common/yesselmanlab/ewhiting/data/rasp_data/human/json_files"
report_path = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/rasp_data/human"

headers = "algo_name, datapoint_name, sequence, prediction, accuracy, p_value\n"

json_files = os.listdir(json_dir)

for jf in json_files:
    ch = jf.replace("_exons.json", "")
    print(f"Workign {ch}")
    report_file = open(f"{report_path}/Simfold_{ch}_report.txt", "w")
    report_file.write(headers)
    with open(f"{json_dir}/{jf}") as fh:
        data = json.load(fh)

    for dp in data:
        name = dp["name"]
        if not os.path.exists(f"{pred_path}/{name}.fasta.dbn"):
            continue

        with open(f"{pred_path}/{name}.fasta.dbn") as fh:
            try:
                dbn_data = fh.readlines()
            except:
                continue

        if len(dbn_data) <= 1:
            continue

        pred_data = dbn_data[1].split(" ")

        if len(pred_data) <= 1:
            continue

        prediction = pred_data[1]
        seq = dp["sequence"].upper().replace("T", "U")

        if len(seq) != len(prediction):
            continue

        reactivity_map = dp["reactivity_map"]
        testable_seq = ""
        testable_dbn = ""
        reactivities = [float(d[1]) for d in reactivity_map]
        for i, _reactivity in reactivity_map:
            testable_seq += seq[i]
            testable_dbn += prediction[i]

        score = DSCI.score(
            testable_seq,
            testable_dbn,
            reactivities,
            DMS=True
        )

        accuracy = score["accuracy"]
        p = score["p"]

        line_to_write = f"Simfold, {name}, {seq}, {prediction}, {accuracy}, {p}\n"
        report_file.write(line_to_write)

    print(f"Finished {ch}")

print("Done")
