import os


# bprna_master_file_0_canonical.txt.100000
base_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions"

for lenience in [0, 1]:
    print(f"Parsing {lenience}-lenience files")
    main_file = open(f"{base_dir}/canonical_bprna_master_file_{lenience}.txt", "w")
    files = [f for f in os.listdir(base_dir) if f"bprna_master_file_{lenience}_canonical.txt" in f]
    for f in files:
        with open(f"{base_dir}/{f}") as fh:
            lines = fh.readlines()
        lines.pop(0)
        main_file.write("".join(lines))

print("Done")
