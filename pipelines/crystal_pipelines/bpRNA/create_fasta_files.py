import os

def sequence_to_file(name, sequence, base_path="/common/yesselmanlab/ewhiting/data/bprna/fasta_files"):
    # Make the name safe to be a filename
    file_safe_name = "".join(c for c in name if c.isalnum() or c == "_")
    if len(file_safe_name) > 200:
        file_safe_name = file_safe_name[0:200]
    data = f">{file_safe_name}\n{sequence}"
    f = open(f"{base_path}/{file_safe_name}.fasta", "w")
    f.write(data)
    f.close()


filtered_dbn_path = "/common/yesselmanlab/ewhiting/data/bprna/dbnFiles/filtered"

# Example DBN file:
# #Name: bpRNA_CRW_50673
# #Length:  77
# #PageNumber: 1
# GGCUGGGUAGCUCAGUUGGUACGAGCGAUCGCCUGAAAAGCGAUAGGUCGCCGGUUCGACCCCGGCCCCAGCCACAA
# (((((((..((((.........))))((((((.......))))))....(((((.......))))))))))))....


new_fasta_path = "/common/yesselmanlab/ewhiting/data/bprna/fasta_files"

dbn_files = os.listdir(filtered_dbn_path)
counter = 0
len_files = len(dbn_files)
for df in dbn_files:
    if not df.endswith(".dbn"):
        continue
    if counter % 250 == 0:
        print(f"Completed {counter} of {len_files} files")
    full_path = f"{filtered_dbn_path}/{df}"
    f = open(full_path)
    data = f.readlines()
    f.close()
    if len(data) != 5:
        print(f"Skipping {df} for weird file format")
        continue
    name = data[0].split("#Name: ")[1].strip()
    sequence = data[3].strip()
    sequence_to_file(name, sequence)
    counter += 1
