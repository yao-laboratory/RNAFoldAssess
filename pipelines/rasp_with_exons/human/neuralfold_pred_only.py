import os, json


"""
cd /common/yesselmanlab/ewhiting/neuralfold_scripts
for ff in $(ls /common/yesselmanlab/ewhiting/data/rasp_data/fasta_files_gt_10/$directory | grep fasta); do
    python ../Neuralfold/NEURALfold.py test /common/yesselmanlab/ewhiting/data/rasp_data/fasta_files_gt_10/$directory/$ff > ./outputs/rasp/$directory/$ff.dbn
done
"""

species = "human"
nf_path = "/common/yesselmanlab/ewhiting/Neuralfold/NEURALfold.py"
output_dir = "/work/yesselmanlab/ewhiting/neuralfold_outputs/rasp/human"
base_dir = "/common/yesselmanlab/ewhiting/data/rasp_data"
json_dir = f"{base_dir}/{species}/json_files"
json_files = os.listdir(json_dir)
ch_map = {}
for jf in json_files:
    ch = jf.replace("_exons.json", "")
    with open(f"{json_dir}/{jf}") as fh:
        ch_map[ch] = json.load(fh)

headers = "algo_name, datapoint_name, sequence, prediction, accuracy, p_value\n"
model_name = "NeuralFold"

completed_exons = []
for dbn_file in os.listdir(output_dir):
    dp_name = dbn_file[:-4]
    completed_exons.append(dp_name)

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
        name = dp["name"]
        if name in completed_exons:
            continue
        sequence = dp["sequence"]
        fasta_string = f">{name}\n{sequence}"
        with open(f"/scratch/{name}.fasta", "w") as fh:
            fh.write(fasta_string)
        cmd = f"python {nf_path} test /scratch/{name}.fasta > {output_dir}/{name}.dbn"
        os.system(cmd)

