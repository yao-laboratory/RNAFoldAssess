import os, shutil


base_dir = "/common/yesselmanlab/ewhiting/spot_outputs/rasp"


species = ["covid", "ecoli", "hiv"]


for s in species:
    print(f"Working {s}")
    ct_path = f"{base_dir}/{s}"
    ct_files = os.listdir(ct_path)
    for cf in ct_files:
        new_name = cf.split(" ")[0] + ".ct"
        shutil.move(f"{ct_path}/{cf}", f"{ct_path}/{new_name}")
