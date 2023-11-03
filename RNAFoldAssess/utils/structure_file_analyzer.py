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
        print(f"Couldn't find secondary structure data in {path}")
        return "no structure"
    ss_data = ss_data.split("\n")
    # Remove empty strings
    ss_data = [d for d in ss_data if d]
    sequence = []
    structure = []
    for i in range(len(ss_data)):
        if "[chain]" in ss_data[i]:
            try:
                sequence.append(ss_data[i+1])
                structure.append(ss_data[i+2])
            except:
                print(f"Anomaly in {file}")
                return "weird file"

    if structure == []:
        # This means that nothing was in the secondary structure section
        # print(f"Bad parse in {path}")
        return "bad parse"

    for s in structure:
        opens = s.count("(")
        closes = s.count(")")
        if opens != closes:
            # For logging
            # print(f"Mismatch in {path} - {opens} '(', {closes} ')'")
            return "mismatch"
    return sequence, structure


base_path = "/common/yesselmanlab/ewhiting/data/crystal1_XRAY/secondary_structure"
mismatches = 0
mismatch_files = []
bad_file_count = 0
bad_files = []
weird_file_count = 0
weird_files = []
bad_parse = 0
bad_parse_files = []
dirs = os.listdir(base_path)
counter = 0
for file in dirs:
    if counter % 150 == 0:
        print(f"Completed {counter} of {len(dirs)}")
    counter += 1
    matching = parse_file(f"{base_path}/{file}")
    if matching == "bad parse":
        bad_parse += 1
        bad_parse_files.append(file)
    if matching == "mismatch":
        mismatches += 1
        mismatch_files.append(file)
    if matching == "no structure":
        bad_file_count += 1
        bad_files.append(file)
    if matching == "weird file":
        weird_file_count += 1
        weird_files.append(file)

print(f"Chains with open bonds: {mismatches}")
print(f"No secondary structure data: {bad_file_count}")
print(f"Anomalous files: {weird_file_count}")

# print("\nwriting bad files...")
# f = open("bad_files.txt", "w")
# for bf in bad_files:
#     f.write(f"{bf}\n")
# f.close()

# print("\nwriting mismatched files...")
# f = open("files_with_mismatched_chains.txt", "w")
# for mf in mismatch_files:
#     f.write(f"{mf}\n")

# print("Done")



