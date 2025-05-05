import json, os


from RNAFoldAssess.models.scorers import *


# Use DMS for ara

pred_path = "/common/yesselmanlab/ewhiting/neuralfold_scripts/outputs"

base_dir = "/common/yesselmanlab/ewhiting/data/rasp_data"
json_dir = f"{base_dir}/ara-tha/json_files"

report_path = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/rasp_data/ara-tha"
headers = "algo_name, datapoint_name, sequence, prediction, accuracy, p_value\n"

json_files = os.listdir(json_dir)

for jf in json_files:
    chromosome_name = jf.replace("_exons.json", "")
    pred_dir = f"{pred_path}/{chromosome_name}"
    json_path = f"{json_dir}/{jf}"
    with open(json_path) as fh:
        data = json.load(fh)
    
    print(f"Working {chromosome_name}")
    report_file = open(f"{report_path}/NeuralFold_{chromosome_name}_report.txt", "w")
    report_file.write(headers)

    for dp in data:
        dbn_path = f"{pred_dir}/{dp['name']}.fasta.dbn"
        with open(dbn_path) as fh:
            dbn_data = fh.readlines()
        
        if len(dbn_data) < 3:
            continue
        prediction = dbn_data[3].strip()

        reactivity_map = dp["reactivity_map"]
        testable_reactivities = [r for _, r in reactivity_map]
        testable_sequence = "".join([dp["sequence"][i] for i, _ in reactivity_map])
        testable_dbn = "".join([prediction[i] for i, _ in reactivity_map])
        # Hello
        score = DSCI.score(
            testable_sequence,
            testable_dbn,
            testable_reactivities,
            DMS=True
        )

        acc = score["accuracy"]
        p = score["p"]

        name = dp["name"]
        seq = dp["sequence"]

        line = f"NeuralFold, {name}, {seq}, {prediction}, {acc}, {p}\n"
        
        report_file.write(line)
    
    report_file.close()