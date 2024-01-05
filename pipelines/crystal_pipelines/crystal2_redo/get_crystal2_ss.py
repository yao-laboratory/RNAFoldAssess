import os

from RNAFoldAssess.utils import *


base_data_path = "/common/yesselmanlab/ewhiting/data/crystal2"
rna_only_data = f"{base_data_path}/rna_only"
with_protein_data = f"{base_data_path}/with_protein"

base_destination_path = "/common/yesselmanlab/ewhiting/data/crystal2/secondary_structures"
rna_only_destination = f"{base_destination_path}/rna_only"
with_protein_destination = f"{base_destination_path}/with_protein"


rna_only_files = [f for f in os.listdir(rna_only_data) if f.split(".")[-1] == "pdb"]
with_protein_files = [f for f in os.listdir(with_protein_data) if f.split(".")[-1] == "pdb"]

print("Starting DSSR on RNA Only PDBs")
for f in rna_only_files:
    DSSR.get_ss_from_pdb(f"{rna_only_data}/{f}", rna_only_destination)

print("Starting DSSR on with-protein PDBs")
for f in with_protein_files:
    DSSR.get_ss_from_pdb(f"{with_protein_data}/{f}", with_protein_destination)
