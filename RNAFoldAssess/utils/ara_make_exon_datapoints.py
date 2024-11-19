import os, json, ast


json_path = "/common/yesselmanlab/ewhiting/data/rasp_data/processed/arabidopsis/round2"
base_path = "/common/yesselmanlab/ewhiting/data/rasp_data/ara-tha"
seq_path = f"{base_path}/fixed_sequences"
cooordinate_path = f"{base_path}/coordinate_files"
assemble_path = f"{base_path}/assemble_files"
dest_dir = f"{base_path}/fixed_sequences"


assemble_files = os.listdir(assemble_path)

print("Assembling datapoints")
ch_dp_map = {}
for json_file in os.listdir(json_path):
    ch_name = json_file.split(".")[0].replace("rasp_arabidopsis_", "")
    # Done with MT already
    if ch_name == "chromosome_Mt":
        continue
    ch_dp_map[ch_name] = {}
    with open(f"{json_path}/{json_file}") as gh:
        dp_data = json.load(gh)
    try:
        for dp in dp_data:
            relevant_data = {
                "sequence": dp["sequence"],
                "data": dp["data"],
                "coordinates": dp["coordinates"]
            }
            ch_dp_map[ch_name][dp["name"]] = relevant_data
    except Exception as e:
        print(f"Problem in {ch_name} -> {dp['name']}: {e}")
        continue


# an exon datapoint should look like this
# exon = {
#     "name": "AT1Gsomething",
#     "sequence": "ACUGUGUGAUAGUUGAUGAUGA",
#     "chem_map_type": "DMS",
#     "reactivity": [(0, 0.4), (5, 0.7)]
# }

json_path_dir = "/common/yesselmanlab/ewhiting/data/rasp_data/ara-tha/json_files"
print("Making datapoints")
for ch in ch_dp_map:
    print(f"\tWorking {ch}")
    new_datapoints = []
    datapoints = ch_dp_map[ch]
    with open(f"{seq_path}/{ch}.seq") as fh:
        chromosome_sequence = fh.read().strip()
    with open(f"{cooordinate_path}/{ch}.coords") as fh:
        lines = fh.readlines()
    for i in range(0, len(lines), 2):
        try:
            exon_name = lines[i].strip()
            coordinates = lines[i+1].strip()
            coordinates = [int(c) for c in coordinates.split(",")]
            sequence = ""
            for c in coordinates:
                sequence += chromosome_sequence[c]
            pos_reads = []
            for dp in datapoints.values():
                for i, reactivity in enumerate(dp["data"]):
                    coordinate = dp["coordinates"][i]
                    if coordinate in coordinates:
                        exon_seq_location = coordinates.index(coordinate)
                        pos_reads.append([exon_seq_location, reactivity])
            if len(pos_reads) <= 0:
                continue
            new_datapoints.append({
                "name": exon_name,
                "sequence": sequence,
                "chem_map_type": "DMS",
                "reactivity_map": pos_reads
            })
        except Exception as e:
            print(f"Problem in {ch}: {e}\nLine is: {lines[i]}")
            continue

    if len(new_datapoints) > 0:
        with open(f"{json_path_dir}/{ch}_exons.json", "w") as fh:
            json.dump(new_datapoints, fh)

