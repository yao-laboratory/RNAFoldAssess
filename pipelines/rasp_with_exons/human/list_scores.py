import os


base_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/rasp_data/human/fixed_files"

report_files = os.listdir(base_dir)

for rf in report_files:
    with open(f"{base_dir}/{rf}") as fh:
        lines = fh.readlines()

    lines = [line.split(", ") for line in lines]
    accs = [float(l[4]) for l in lines]

    avg = sum(accs) / len(accs)
    mname = rf.split("_")[0]
    print(f"{mname}\t\t{avg}")
