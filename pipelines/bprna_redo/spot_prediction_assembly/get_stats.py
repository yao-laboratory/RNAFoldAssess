import os


base_dir = "/work/yesselmanlab/ewhiting/bprna_preds/redo_reports"

for lenience in [0, 1]:
    with open(f"{base_dir}/SPOT-RNA_master_{lenience}_lenience.txt") as fh:
        data = fh.readlines()
    data.pop(0)
    sens = []
    ppvs = []
    f1s = []
    for d in data:
        d = d.split(", ")
        # 6, 7, 8
        s = float(d[6].strip())
        p = float(d[7].strip())
        f = float(d[8].strip())
        sens.append(s)
        ppvs.append(p)
        f1s.append(f)
    n = len(sens)
    print(f"for lenience {lenience}, n of {n}:")
    print(f"\tSensitivity: {sum(sens) / len(sens)}")
    print(f"\tPPV: {sum(ppvs) / len(ppvs)}")
    print(f"\tF1: {sum(f1s) / len(f1s)}")
