import os

def sequence_to_file(name, sequence):
    # To seq file
    name = name.replace(" ", "_")
    name = name.replace("/", "")
    name = name.replace("'", "")
    name = name.replace("(", "")
    name = name.replace(")", "")
    name = name.replace("[", "")
    name = name.replace("]", "")
    name = name.replace("{", "")
    name = name.replace("}", "")
    name = name.replace("<", "")
    name = name.replace(">", "")
    name = name.replace(";", "")
    name = name.replace(",", "")
    name = name.replace("|", "")
    name = name.replace("`", "")
    name = name.replace('"', "")
    name = name.replace("$", "S")
    name = name.replace("&", "and")
    name = name.replace("~", "")
    if len(name) > 200:
        name = name[0:200]
    f = open(f"{name}.seq", "w")
    f.write(sequence)
    f.close()
    path = os.path.abspath(f"{name}.seq")
    return path


dbn_path = "/common/yesselmanlab/ewhiting/data/bprna/dbnFiles"
seq_destination = "/common/yesselmanlab/ewhiting/data/bprna/seq_files"
files = os.listdir(dbn_path)
file_len = len(files)

counter = 0
for file in files:
    if counter % 125 == 0:
        print(f"Completed {counter} files")
    dbn_file = open(f"{dbn_path}/{file}")
    data = dbn_file.readlines()
    dbn_file.close()
    if len(data) != 5:
        print(f"Skipping {file} for weird file format")
        skipped += 1
        continue
    name = data[0].split("#Name: ")[1].strip()
    sequence = data[3].strip()
    sequence_to_file(name, sequence)
    counter += 1

