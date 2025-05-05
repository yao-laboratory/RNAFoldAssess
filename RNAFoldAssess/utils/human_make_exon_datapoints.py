import os, json, ast


json_path = "/common/yesselmanlab/ewhiting/data/rasp_data/human/processed"
base_path = "/common/yesselmanlab/ewhiting/data/rasp_data/human"
seq_path = f"{base_path}/fixed_sequences"
cooordinate_path = f"{base_path}/coordinate_files"

# There's only data for 1, 2, 18, and 19
available_chromosomes = [
    "chr1",
    "chr2",
    # "chr18", # Already done
    "chr19",
]

print("Assembling datapoints")
ch_dp_map = {}
json_files = [f for f in os.listdir(json_path) if f.endswith(".json")]
for json_file in json_files:
    ch_name = json_file.split(".")[0].replace("rasp_human_chromosome_", "")
    if ch_name not in available_chromosomes:
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

json_path_dir = "/common/yesselmanlab/ewhiting/data/rasp_data/human/json_files"
print("Making datapoints")
for ch in ch_dp_map:
    print(f"\tWorking {ch}")
    new_datapoints = []
    datapoints = ch_dp_map[ch]
    with open(f"{seq_path}/{ch}.seq") as fh:
        chromosome_sequence = fh.read().strip()
    with open(f"{cooordinate_path}/chromosome_{ch}.coords") as fh:
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

