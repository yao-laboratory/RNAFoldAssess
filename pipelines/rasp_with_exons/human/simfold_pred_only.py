# /common/yesselmanlab/ewhiting/simfold_scripts

import os, json

species = "human"
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
    data = ch_map[ch]
    counter = 0
    len_data = len(data)
    for dp in data:
        counter += 1
        if counter % 250 == 0:
            print(f"Working {counter} of {len_data}")
        if len(dp["sequence"]) < 10:
            continue
        sequence = dp["sequence"]
        name = dp["name"]
        cmd = f'../simfold/simfold -s "{sequence}" > outputs/rasp/{species}/{name}.dbn'
        os.system(cmd)

