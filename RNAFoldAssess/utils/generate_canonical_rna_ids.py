from pdb_tools import PDBTools

# canonical_ids = PDBTools.get_canonical_pdb_ids("/common/yesselmanlab/ewhiting/data/with_protein_ids.txt")
# f = open("./canonical_ids_with_protein", "w")
# for id in canonical_ids:
#     f.write(f"{id}\n")
# f.close()

# f = open("./canonical_ids_with_protein", "r")
# pdb_ids = f.readlines()
# f.close()

destination_dir = "/common/yesselmanlab/ewhiting/data/crystal2/with_protein/"
for pdb_id in pdb_ids:
    PDBTools.get_pdb_file(pdb_id.strip(), destination_dir)
    PDBTools.get_mmcif_file(pdb_id.strip(), destination_dir)

# Note: everything is commented out because I did this part very haphazardly

