import os


destination_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/consolidated"

file_names = [
    "bp-RNA_all_datapoints.csv",
    "EternaBench_all_datapoints.csv",
    "PDB_all_datapoints.csv",
    "RASP-Arabidopsis_all_datapoints.csv",
    "RASP-COVID_all_datapoints.csv",
    "RASP-ecoli_all_datapoints.csv",
    "RASP-HIV_all_datapoints.csv",
    "RASP-Human_all_datapoints.csv",
    "Ribonanza_all_datapoints.csv",
    "RNAndria-miRNA_all_datapoints.csv",
    "RNAndria-mRNA_all_datapoints.csv",
    "YData_all_datapoints.csv"
]

def get_gc_content(seq):
    gs = seq.count("G") + seq.count("g")
    cs = seq.count("C") + seq.count("c")
    gc_content = (gs + cs) / len(seq)
    return gc_content


for fn in file_names:
    print(f"Working {fn}")
    src = f"{destination_dir}/{fn}"
    new_fn = fn.replace(".csv", "_gc.csv")
    dest = f"{destination_dir}/{new_fn}"
    with open(src) as fh:
        lines = fh.readlines()

    headers = lines.pop(0).strip()
    headers += ",gc_content\n"
    f = open(dest, "w")
    f.write(headers)
    for line in lines:
        line = [l.strip() for l in line.split(",")]
        seq = line[2]
        gc_content = get_gc_content(seq)
        line.append(str(gc_content))
        line = ",".join(line) + "\n"
        f.write(line)

    f.close()