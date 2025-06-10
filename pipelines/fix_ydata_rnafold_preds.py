rf = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/ydata/RNAFold_YesselmanDMS_report_backup.txt"

with open(rf) as fh:
    data = fh.readlines()

headers = data.pop(0)

new_data = []

acceptable_cohorts = [
    "C014G",
    "C014H",
    "C014I",
    "C014J",
    "C014U",
    "C014V",
]

data = [d.split(", ") for d in data]

for d in data:
    dp = d[1]
    cohort = dp.split("_")[0]
    if cohort not in acceptable_cohorts:
        continue
    new_data.append(d)


new_data = [", ".join(d) for d in new_data]
new_report_str = "".join(new_data)

with open("/mnt/nrdstor/yesselmanlab/ewhiting/reports/ydata/RNAFold_YesselmanDMS_report.txt", "w") as fh:

    fh.write(new_report_str)
