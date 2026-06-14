import os


base_path = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/crystal_release_2024/canonical"
dest_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/consolidated"
headers = "algo_name, datapoint_name, lenience, sequence, true_structure, prediction, sensitivity, ppv, f1"

leniences = [0, 1]

for lenience in leniences:
    fstring = f"{headers}\n"
    files = [f for f in os.listdir(base_path) if f"{lenience}_lenience.txt" in f]
    for f in files:
        with open(f"{base_path}/{f}") as fh:
            lines = fh.readlines()

        lines.pop(0)
        fstring += "".join(lines)

    with open(f"{dest_dir}/pdb_all_preds_{lenience}_lenience.txt", "w") as fh:
        fh.write(fstring)
