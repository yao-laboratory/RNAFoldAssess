import os

models = [
    "ContextFold",
    "ContraFold",
    "EternaFold",
    "IPKnot",
    "MXFold",
    "MXFold2",
    "RandomPredictor",
    "RNAStructure",
    "RNAFold",
    "SeqFold"
]

datasets = [
    "bprna",
    "eterna_data",
    "rasp_data",
    "ribonanza",
    "rnandria",
    "ydata"
]

detailed_datasets = [
    "bprna",
    "eterna_data",
    "rasp_data_arabidopsis",
    "rasp_data_covid",
    "rasp_data_ecoli",
    "rasp_data_hiv",
    "rasp_data_human",
    "ribonanza",
    "rnandria_pri_miRNA",
    "rnandria_human_mRNA",
    "ydata"
]

model_accuracies = {}

for m in models:
    model_accuracies[m] = {}
    for d in detailed_datasets:
        model_accuracies[m][d] = 0


# Get bpRNA
report_dir = "/common/yesselmanlab/ewhiting/reports/bprna"
for m in models:
    if m == "MXFold2":
        continue
    path = f"{report_dir}/{m}_bpRNA-1m-90_report.txt"
    f = open(path)
    data = f.readlines()
    f.close()
    sens = []
    offset = 0
    for i, d in enumerate(data):
        if offset % 2 == 0:
            offset += 1
            items = d.split(", ")
            sens.append(float(items[5]))
        else:
            continue
    model_accuracies[m]["bpRNA"] = round(sum(sens) / len(sens), 4)


# Get eterna_data
report_dir = "/common/yesselmanlab/ewhiting/reports/eterna_data"
for m in models:
    path = f"{report_dir}/{m}_DMS_pipeline_report.txt"
    f = open(path)
    data = f.readlines()
    f.close()
    accs = []
    data.pop(0)
    for d in data:
        items = d.split(", ")
        acc = float(items[4])
        accs.append(round(acc, 4))
    path = f"{report_dir}/{m}_SHAPE_pipeline_report.txt"
    f = open(path)
    data = f.readlines()
    f.close()
    accs = []
    data.pop(0)
    for d in data:
        items = d.split(", ")
        acc = float(items[4])
        accs.append(round(acc, 4))
    model_accuracies[m]["eterna_data"] = round(sum(accs) / len(accs), 4)


# get rasp data
report_dir = "/common/yesselmanlab/ewhiting/reports/rasp_data"
species = [
    "arabidopsis",
    "covid",
    "ecoli",
    "hiv",
    "human"
]

for s in species:
    if s == "hiv":
        nf = "HIV"
    else:
        nf = s
    s_report_dir = f"{report_dir}/{nf}"
    for m in models:
        if m == "MXFold2":
            continue
        ms_report_dir = f"{report_dir}/{nf}/{m}"
        print(ms_report_dir)
        files = os.listdir(ms_report_dir)
        files = [f for f in files if f.endswith("predictions.txt")]
        accs = []
        for fp in files:
            f = open(f"{ms_report_dir}/{fp}")
            data = f.readlines()
            f.close()
            data.pop(0)
            for d in data:
                items = d.split(", ")
                acc = float(items[4])
                accs.append(acc)
        if len(accs) > 0:
            model_accuracies[m][f"rasp_data_{s}"] = sum(accs)/len(accs)


# Get Ribonanza
report_dir = "/common/yesselmanlab/ewhiting/reports/ribonanza"
all_files = os.listdir(report_dir)
all_files = [f for f in all_files if f.endswith("predictions.txt")]
for m in models:
    accs = []
    mfiles = [f for f in all_files if f.startswith(m)]
    for ff in mfiles:
        f = open(f"{report_dir}/{ff}")
        data = f.readlines()
        f.close()
        for d in data:
            items = d.split(", ")
            acc = float(items[4])
            accs.append(acc)
    if len(accs) > 0:
        model_accuracies[m]["ribonanza"] = round(sum(accs) / len(accs), 4)


# Get RNAndria
report_dir = "/common/yesselmanlab/ewhiting/reports/rnandria"
for m in models:
    if m == "MXFold2":
        continue
    pff = f"{report_dir}/{m}_rnandria_pri_miRNA_predictions.txt"
    f = open(pff)
    data = f.readlines()
    f.close()
    p_accs = []
    for d in data:
        items = d.split(", ")
        acc = float(items[4])
        p_accs.append(acc)
    # Human
    hff = f"{report_dir}/{m}_rnandria_human_mRNA_predictions.txt"
    f = open(hff)
    data = f.readlines()
    f.close()
    h_accs = []
    for d in data:
        items = d.split(", ")
        acc = float(items[4])
        h_accs.append(acc)
    if len(p_accs) > 0:
        model_accuracies[m]["rnandria_pri_miRNA"] = round(sum(p_accs) / len(p_accs), 4)
    if len(h_accs) > 0:
        model_accuracies[m]["rnandria_human_mRNA"] = round(sum(h_accs) / len(h_accs), 4)


# Get ydata
report_dir = "/common/yesselmanlab/ewhiting/reports/ydata"
for m in models:
    if m == "IPKnot":
        nm = "IPknot"
    else:
        nm = m
    f = open(f"{report_dir}/{nm}_YesselmanDMS_report.txt")
    data = f.readlines()
    f.close()
    accs = []
    data.pop(0)
    for d in data:
        items = d.split(", ")
        acc = float(items[4])
        accs.append(acc)
    model_accuracies[m]["ydata"] = round(sum(accs) / len(accs), 4)


rf = open("all_model_accuracies.txt", "w")
wrote_column = False
line_to_write = ""
for m in model_accuracies:
    ss = model_accuracies[m]
    print(m)
    if not wrote_column:
        line_to_write += "\t"
        for i in ss:
            line_to_write += f"{i}\t"
        line_to_write += "\n"
        wrote_column = True
    line_to_write += f"{m}\t"
    for i in ss:
        print(f"  {i}: {ss[i]}")
        line_to_write += f"{ss[i]}\t"
    line_to_write += "\n"

rf.write(line_to_write)
rf.close()
