import os, json


from RNAFoldAssess.models.scorers import *


headers = "algo_name, datapoint_name, sequence, prediction, accuracy, p_value\n"
dbn_file_loc = "/common/yesselmanlab/ewhiting/spot_outputs/rasp/human/dbn_files/formatted"
json_dir = "/common/yesselmanlab/ewhiting/data/rasp_data/human/json_files"

json_files = os.listdir(json_dir)

ch_map = {}
for jf in json_files:
    ch = jf.replace("_exons.json", "")
    with open(f"{json_dir}/{jf}") as fh:
        ch_map[ch] = json.load(fh)

for ch, dps in ch_map.items():
    print(f"Working {ch}")
    report_file = open(f"/mnt/nrdstor/yesselmanlab/ewhiting/reports/rasp_data/human/SPOT-RNA_{ch}_report.txt", "w")
    report_file.write(headers)
    for dp in dps:
        name = dp["name"]
        pred_path = f"{dbn_file_loc}/{name}.ct.dbn"
        if not os.path.exists(pred_path):
            continue

        with open(pred_path) as fh:
            dbn_data = [line.strip() for line in fh.readlines()]

        prediction = dbn_data[2]
        seq = dbn_data[1]

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

        acc = score["accuracy"]
        p = score["p"]

        line_to_write = f"SPOT-RNA, {dp['name']}, {seq}, {prediction}, {acc}, {p}\n"
        report_file.write(line_to_write)

    report_file.close()
