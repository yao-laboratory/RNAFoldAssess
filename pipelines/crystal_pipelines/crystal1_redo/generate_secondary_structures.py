import os

from RNAFoldAssess.utils import *


base_dir = "/common/yesselmanlab/ewhiting/data/crystal1_XRAY"
pdb_list = f"{base_dir}/redo_analysis/raw_list.txt"
destination = f"{base_dir}/redo_analysis/secondary_structures"

f_pdb_list = open(pdb_list)
pdbs = [pdb.strip() for pdb in f_pdb_list.readlines()]

for pdb in pdbs:
    loc = f"{base_dir}/{pdb}.pdb"
    DSSR.get_ss_from_pdb(loc, destination)
