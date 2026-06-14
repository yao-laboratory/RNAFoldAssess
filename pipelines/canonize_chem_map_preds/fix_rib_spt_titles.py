import os, shutil

from_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/spot_scripts/ribonanza"
to_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/spot_outputs/ribonanza/fixed_title"

files_to_change = os.listdir(from_dir)

counter = 0
for f in files_to_change:
    counter += 1
    if counter % 678 == 0:
        print(f"Working {counter} of {len(files_to_change)}")
    dp_name = f.split(" ")[0]
    new_file_name = f"{dp_name}.ct"
    shutil.copy(f"{from_dir}/{f}", f"{to_dir}/{new_file_name}")

