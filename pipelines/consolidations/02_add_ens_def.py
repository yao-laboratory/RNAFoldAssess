# go to /common/yesselmanlab/ewhiting/vienna

import vienna


destination_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/consolidated"

file_names = [
    "bp-RNA_all_datapoints_gc.csv",
    "EternaBench_all_datapoints_gc.csv",
    "PDB_all_datapoints_gc.csv",
    "RASP-Arabidopsis_all_datapoints_gc.csv",
    "RASP-COVID_all_datapoints_gc.csv",
    "RASP-ecoli_all_datapoints_gc.csv",
    "RASP-HIV_all_datapoints_gc.csv",
    "RASP-Human_all_datapoints_gc.csv",
    "Ribonanza_all_datapoints_gc.csv",
    "RNAndria-miRNA_all_datapoints_gc.csv",
    "RNAndria-mRNA_all_datapoints_gc.csv",
    "YData_all_datapoints_gc.csv"
]

def get_ed_and_mfe(seq):
    fr = vienna.fold(seq)
    ens_defect = fr.ens_defect
    mfe = fr.mfe
    return f"{ens_defect},{mfe}\n"


for fn in file_names:
    print(f"Working {fn}")
    new_fn = fn.replace(".csv", "_ed_mfe.csv")
    src = f"{destination_dir}/{fn}"
    dest = f"{destination_dir}/{new_fn}"
    with open(src) as fh:
        lines = fh.readlines()

    headers = lines.pop(0).strip()
    headers += ",ensemble_defect,min_free_energy\n"
    f = open(dest, "w")
    for line in lines:
        line = [l.strip() for l in line.split(",")]
        seq = line[2]
        line = ",".join(line)
        new_str = get_ed_and_mfe(seq)
        line += new_str
        f.write(line)
    f.close()