import os

crystal1_list = open("/common/yesselmanlab/ewhiting/data/crystal1_XRAY/redo_analysis/raw_list.txt")
crystal2_rna_list = open("/common/yesselmanlab/ewhiting/data/crystal2/rna_only_list.txt")
crystal2_protein_list = open("/common/yesselmanlab/ewhiting/data/crystal2/with_protein_list.txt")

crystal1 = [pdb.strip() for pdb in crystal1_list.readlines()]
crystal1_list.close()
crystal2_rna = [pdb.strip() for pdb in crystal2_rna_list.readlines()]
crystal2_rna_list.close()
crystal2_protein = [pdb.strip() for pdb in crystal2_protein_list.readlines()]
crystal2_protein_list.close()

def get_shared(comp):
    shared = []
    for pdb in comp:
        if pdb in crystal1:
            shared.append(pdb)
    return shared

c2r = get_shared(crystal2_rna)
c2p = get_shared(crystal2_protein)

print(f"Dataset Crystal2 - RNA Only has {len(c2r)} of {len(crystal2_rna)} PDBs in common with Dataset Crystal1:")
print(f"Dataset Crystal2 - With Protein has {len(c2p)} of {len(crystal2_protein)} PDBs in common with Dataset Crystal1:")

def write_uniq(dataset, destination):
    uniques = []
    for pdb in dataset:
        if pdb not in crystal1:
            uniques.append(pdb)
    f = open(destination, "w")
    for pdb in uniques:
        f.write(f"{pdb}\n")
    f.close()
    print(f"Wrote {len(uniques)} IDs to {destination}")


c2r_destination = f"/common/yesselmanlab/ewhiting/data/crystal2/rna_only_unique.txt"
c2p_destination = f"/common/yesselmanlab/ewhiting/data/crystal2/with_protein_unique.txt"

write_uniq(crystal2_rna, c2r_destination)
write_uniq(crystal2_protein, c2p_destination)
