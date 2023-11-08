import os
# Parsing through the ss files

asterisks = "****************************************************************************"
ss_string = "Secondary structures"

def parse_file(path):
    f = open(path)
    raw_data = f.read()
    f.close()
    data = raw_data.split(asterisks)
    ss_data = None
    for d in data:
        if ss_string in d:
            ss_data = d
            break
    if not ss_data:
        raise Exception(f"No secondary structure in {path}")
    ss_data = ss_data.split("\n")
    whole_seq = ""
    whole_structure = ""
    chains = []
    for i in range(len(ss_data)):
        if "[whole]" in ss_data[i]:
            whole_seq = ss_data[i+1]
            whole_structure = ss_data[i+2]
        if "[chain]" in ss_data[i]:
            chain_id = ss_data[i].split("-")[1].split(" ")[0]
            chains.append({
                "chain_id": chain_id,
                "sequence": ss_data[i+1],
                "structure": ss_data[i+2]
            })
    return {
        "name": path.split(".")[0].split("/")[-1],
        "sequence": whole_seq,
        "structure": whole_structure,
        "chains": chains
    }


# For testing
# test_file = "/common/yesselmanlab/ewhiting/data/crystal1_XRAY/secondary_structure/5AH5.ss"
# val = parse_file(test_file)

base_ss_data_path = "/common/yesselmanlab/ewhiting/data/crystal1_XRAY/secondary_structure"
files = os.listdir(base_ss_data_path)

structure_data = []
print("assembling data ...")
for f in files:
    # Ignore weirdly named file:
    if f == ".ss":
        continue
    structure_data.append(
        parse_file(f"{base_ss_data_path}/{f}")
    )

def write_data_to_file(data, split_tolerance=1):
    counter = 0
    length = len(data)
    all_structures = open("whole_crystal_structures.txt", "w")
    sf_records = 0
    af_records = 0
    pf_records = 0
    for d in data:
        if counter % 200 == 0:
            print(f"Completed {counter} of {length}")
        seq = d["sequence"]
        ss = d["structure"]
        text = f">{d['name']}\n{seq}\n{ss}\n"
        all_structures.write(text)
        counter += 1
    all_structures.close()


print("writing files ...")
write_data_to_file(structure_data)
