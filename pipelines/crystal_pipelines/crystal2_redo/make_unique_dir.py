import os

r_uniques_path = "/common/yesselmanlab/ewhiting/data/crystal2/rna_only_unique.txt"
p_uniques_path = "/common/yesselmanlab/ewhiting/data/crystal2/with_protein_unique.txt"

r_data_path = "/common/yesselmanlab/ewhiting/data/crystal2/secondary_structures/rna_only"
p_data_path = "/common/yesselmanlab/ewhiting/data/crystal2/secondary_structures/with_protein"

destination_base = "/common/yesselmanlab/ewhiting/data/crystal2/secondary_structures"
r_dest = f"{destination_base}/rna_only/uniques"
p_dest = f"{destination_base}/with_protein/uniques"

def build_unique_directory(unique_list_path, data_path, destination):
    f = open(unique_list_path)
    uniques = [pdb.strip() for pdb in f.readlines()]
    f.close()
    dbs = os.listdir(data_path)
    for file in dbs:
        if file.endswith("dbn") and file[:4] in uniques:
            cmd = f"cp {data_path}/{file} {destination}/{file}"
            os.system(cmd)


build_unique_directory(r_uniques_path, r_data_path, r_dest)
build_unique_directory(p_uniques_path, p_data_path, p_dest)
