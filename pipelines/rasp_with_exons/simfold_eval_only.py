import os, json

from RNAFoldAssess.models.scorers import *

species = "ara-tha"
base_dir = "/common/yesselmanlab/ewhiting/data/rasp_data"
json_dir = f"{base_dir}/{species}/json_files"
json_files = os.listdir(json_dir)
ch_map = {}
for jf in json_files:
    ch = jf.replace("_exons.json", "")
    with open(f"{json_dir}/{jf}") as fh:
        ch_map[ch] = json.load(fh)

headers = "algo_name, datapoint_name, sequence, prediction, accuracy, p_value\n"
model_name = "Simfold"

for ch in ch_map:
    print(f"Working {ch} in {species}")
    report_file = open(f"/mnt/nrdstor/yesselmanlab/ewhiting/reports/rasp_data/{species}/{model_name}_{ch}_preds.txt", "w")
    report_file.write(headers)

    data = ch_map[ch]
    counter = 0
    len_data = len(data)
    for dp in data:
        counter += 1
        if counter % 250 == 0:
            print(f"Working {counter} of {len_data}")
        if len(dp["sequence"]) < 10:
            continue
        try:
            chem_map_method = dp["chem_map_type"]
            sequence = dp["sequence"]
            name = dp["name"]
            pred_file = f"outputs/rasp/{species}/{name}.dbn"
            with open(pred_file) as fh:
                pred_data = fh.readlines()
            dbn_line = pred_data[-1].strip()
            dbn = dbn_line.split(" ")[1]
            reactivity_map = dp["reactivity_map"]
            indexes = [i[0] for i in reactivity_map]
            reactivities = [i[1] for i in reactivity_map]
            testable_sequence = "".join([sequence[i] for i in indexes])
            testable_dbn = "".join([dbn[i] for i in indexes])

            if chem_map_method == "DMS":
                score = DSCI.score(
                    testable_sequence,
                    testable_dbn,
                    reactivities,
                    DMS=True
                )
            elif chem_map_method == "SHAPE":
                score = DSCI.score(
                    testable_sequence,
                    testable_dbn,
                    reactivities,
                    SHAPE=True
                )

            accuracy = score["accuracy"]
            p = score["p"]
            line_to_write = f"{model_name}, {dp['name']}, {dp['sequence']}, {dbn}, {accuracy}, {p}\n"
            report_file.write(line_to_write)
        except Exception as e:
            print(f"Exception on {dp['name']}: {e}")

    report_file.close()
    print(f"Finished {ch}")
