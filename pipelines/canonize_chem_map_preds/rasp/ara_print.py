import os

report_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/rasp_data/ara-tha/canonical"

files = os.listdir(report_dir)
for f in files:
    model = f.split("_")[0]
    with open(f"{report_dir}/{f}") as fh:
        lines = fh.readlines()

    lines = [line.split(", ") for line in lines]
    accs = [float(d[4]) for d in lines]
    avg = sum(accs) / len(accs)
    print(f"{model} - {avg}, n = {len(accs)}")
