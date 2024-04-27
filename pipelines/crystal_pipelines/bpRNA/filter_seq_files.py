import os


base = "/common/yesselmanlab/ewhiting/data/bprna/dbnFiles/filtered"
destination = "/common/yesselmanlab/ewhiting/data/bprna/seq_files_filtered"


def sequence_to_file(name, sequence, dest_path="/common/yesselmanlab/ewhiting/data/bprna/seq_files_filtered"):
    # Make the name safe to be a filename
    file_safe_name = "".join(c for c in name if c.isalnum() or c == "_")
    if len(file_safe_name) > 200:
        file_safe_name = file_safe_name[0:200]
    f = open(f"{dest_path}/{file_safe_name}.seq", "w")
    f.write(sequence)
    f.close()


dbn_files = os.listdir(base)
dbn_files = [s for s in dbn_files if s.endswith(".dbn")]
len_files = len(dbn_files)

# Example DBN file:
# #Name: bpRNA_CRW_50673
# #Length:  77
# #PageNumber: 1
# GGCUGGGUAGCUCAGUUGGUACGAGCGAUCGCCUGAAAAGCGAUAGGUCGCCGGUUCGACCCCGGCCCCAGCCACAA
# (((((((..((((.........))))((((((.......))))))....(((((.......))))))))))))....

counter = 0
print("Starting")
for df in dbn_files:
    if counter % 750 == 0:
        print(f"Working {counter} of {len_files}")
    f = open(f"{base}/{df}")
    data = f.readlines()
    f.close()
    if len(data) != 5:
        print(f"Skipping {df} for weird file format")
        continue
    name = data[0].split("#Name: ")[1].strip()
    sequence = data[3].strip()
    sequence_to_file(name, sequence)
    counter += 1

