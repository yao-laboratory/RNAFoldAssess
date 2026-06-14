base_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions"
pred_dirs = [
    f"{base_dir}/canonical_bprna_master_file_0.txt",
    f"{base_dir}/canonical_bprna_master_file_1.txt"
]

for lenience in [0, 1]:
    with open(pred_dirs[lenience]) as fh:
        lines = fh.readlines()
    lines = [line.split(", ") for line in lines]
    # sens, ppv, f1
    sens = [float(line[7]) for line in lines]
    ppvs = [float(line[8]) for line in lines]
    f1s = [float(line[9]) for line in lines]

    print(f"For {lenience} lenience:")
    print(f"Sensitivity: {sum(sens) / len(sens)}")
    print(f"PPVs: {sum(ppvs) / len(ppvs)}")
    print(f"F1s: {sum(f1s) / len(f1s)}")
    print()
