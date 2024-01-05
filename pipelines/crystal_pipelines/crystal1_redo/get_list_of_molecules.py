import os


ss_dir = "/common/yesselmanlab/ewhiting/data/crystal1_XRAY/dssr_output"
destination = "/common/yesselmanlab/ewhiting/data/crystal1_XRAY/redo_analysis"
list_txt = "raw_list.txt"
report_txt = "report.txt"

files = os.listdir(ss_dir)
pdbs = []
for f in files:
    pdb = f.split(".")[0]
    pdbs.append(pdb)


report = open(f"{destination}/{report_txt}", "w")
report.write(f"There are {len(pdbs)} PDB IDs in this dataset\n")
report.close()

raw_list = open(f"{destination}/{list_txt}", "w")
for pdb in pdbs:
    raw_list.write(f"{pdb}\n")
