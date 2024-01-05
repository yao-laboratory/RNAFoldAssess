import os

base_dir = "/common/yesselmanlab/ewhiting/data/crystal2"
rna_only_ss_dir = f"{base_dir}/secondary_structures/rna_only"
with_protein_ss_dir = f"{base_dir}/secondary_structures/with_protein"

r_list = f"{base_dir}/rna_only_list.txt"
w_list = f"{base_dir}/with_protein_list.txt"

r_report = f"{base_dir}/rna_only_report.txt"
w_report = f"{base_dir}/with_protein_report.txt"

def write_report(ss_dir, report_destination, list_destination):
    files = os.listdir(ss_dir)
    pdbs = []
    for f in files:
        pdb = f.split(".")[0]
        pdbs.append(pdb)

    report = open(report_destination, "w")
    report.write(f"There are {len(pdbs)} PDB IDs in this dataset\n")
    report.close()
    raw_list = open(list_destination, "w")
    for pdb in pdbs:
        raw_list.write(f"{pdb}\n")
    raw_list.close()


write_report(rna_only_ss_dir, r_report, r_list)
write_report(with_protein_ss_dir, w_report, w_list)
