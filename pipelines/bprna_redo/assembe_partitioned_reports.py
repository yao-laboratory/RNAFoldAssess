import sys, os

model = sys.argv[1]
report_path = "/work/yesselmanlab/ewhiting/bprna_preds/redo_reports"
headers = "model_name, dp_name, lenience, sequence, true_structure, predicted_structure, sensitivity, ppv, f1\n"

for lenience in [0, 1]:
    reports = [ff for ff in os.listdir(report_path) if f"{model}_" in ff and f"{lenience}_lenience.txt" in ff and "master" not in ff]
    master_data = []
    for report in reports:
        with open(f"{report_path}/{report}") as f:
            data = f.readlines()
        if len(data) == 0:
            continue
        data.pop(0)
        master_data += data
    sens = []
    ppvs = []
    f1s = []
    report = open(f"{report_path}/{model}_master_{lenience}_lenience.txt", "w")
    report.write(headers)
    oops = 0
    for md in master_data:
        try:
           d = md.split(", ")
           sens.append(float(d[6]))
           ppvs.append(float(d[7]))
           f1s.append(float(d[8].strip()))
           report.write(md)
        except Exception as e:
            print(f"Problem with {md}: {e}")
            oops += 1
            continue
    report.close()
    dp_count = len(master_data) - oops
    sen = sum(sens) / len(sens)
    ppv = sum(ppvs) / len(ppvs)
    f1 = sum(f1s) / len(f1s)
    summary_string = f"{model}\nLenience: {lenience}\nDatapoints analyzed: {dp_count}\nSensitivity: {str(sen)}\nPPV: {str(ppv)}\nF1: {str(f1)}\n"
    summary = open(f"{report_path}/{model}_{lenience}_lenience_summary.txt", "w")
    print(summary_string)
    summary.write(summary_string)
    summary.close()

