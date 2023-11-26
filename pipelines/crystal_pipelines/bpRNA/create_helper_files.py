import os

dbn_path = "/common/yesselmanlab/ewhiting/data/bprna/dbnFiles"
files = os.listdir(dbn_path)
file_len = len(files)

helper_path = "/common/yesselmanlab/ewhiting/data/bprna/helper_files"
helper_file = open(f"{helper_path}/data.txt", "w")

dbn_files = os.listdir(dbn_path)

counter = 0
for dbn_file in dbn_files:
    counter += 1
    if counter % 250 == 0:
        print(f"Creating file {counter} of {file_len}")
    f = open(f"{dbn_path}/{dbn_file}")
    data = f.readlines()
    f.close()
    if len(data) != 5:
        print(f"Skipping {file} for weird file format")
        continue
    name = data[0].split("#Name: ")[1].strip()
    data_type = name.split("_")[1]
    sequence = data[3].strip()
    true_structure = data[4].strip()
    fstring = f"{name}\n{data_type}\n{sequence}\n{true_structure}\n\n"
    helper_file.write(fstring)

helper_file.close()
