import os


base_dir = "/common/yesselmanlab/ewhiting/data/crystal1_XRAY"
ss_dir = f"{base_dir}/redo_analysis/secondary_structures"
prep_dir = f"{ss_dir}/preprocessed"
destination_dir = f"{prep_dir}/twenty_plus"

dbns = [dbn for dbn in os.listdir(prep_dir) if dbn.endswith("dbn")]

for dbn in dbns:
    f = open(f"{prep_dir}/{dbn}")
    lines = f.readlines()
    f.close()
    seq = lines[1]
    if len(seq) >= 20:
        cmd = f"cp {prep_dir}/{dbn} {destination_dir}/{dbn}"
        os.system(cmd)
