import os, json, ast


json_path = "/common/yesselmanlab/ewhiting/data/rasp_data/human/processed"
base_path = "/common/yesselmanlab/ewhiting/data/rasp_data/human"
seq_path = f"{base_path}/sequences"
assemble_path = f"{base_path}/assemble_files"
dest_dir = f"{base_path}/fixed_sequences"

if not os.path.exists(dest_dir):
    os.mkdir(dest_dir)

assemble_files = os.listdir(assemble_path)

json_files = [f for f in os.listdir(json_path) if f.endswith(".json")]

print("Assembling datapoints")
ch_dp_map = {}
for json_file in json_files:
    ch_name = json_file.split(".")[0].replace("rasp_human_", "")
    ch_dp_map[ch_name] = {}
    with open(f"{json_path}/{json_file}") as gh:
        dp_data = json.load(gh)
    for dp in dp_data:
        relevant_data = {
            "sequence": dp["sequence"],
            # "data": dp["data"],
            "coordinates": dp["coordinates"]
        }
        ch_dp_map[ch_name][dp["name"]] = relevant_data


print("Creating new sequence files")
for chromosome in ch_dp_map:
    print(f"Working {chromosome}")
    dp_data = ch_dp_map[chromosome]
    assemblies = [f for f in assemble_files if f.startswith(f"{chromosome}_")]
    seq_file_name = chromosome.replace("chromosome_", "")
    sequence_file = f"{seq_path}/{seq_file_name}.seq"
    with open(sequence_file) as fh:
        old_sequence = list(fh.read())
    for assembly in assemblies:
        with open(f"{assemble_path}/{assembly}") as fh:
            assembly_data = [line.strip() for line in fh.readlines()]
        for ad in assembly_data:
            dp_name, _coordinates = ad.split(" - ")
            dp = dp_data[dp_name]
            for i, coordinate in enumerate(dp["coordinates"]):
                old_sequence[coordinate] = dp["sequence"][i]
    new_sequence = "".join(old_sequence)
    new_sequence = new_sequence.replace("T", "U")

    with open(f"{dest_dir}/{seq_file_name}.seq", "w") as fh:
        fh.write(new_sequence)
