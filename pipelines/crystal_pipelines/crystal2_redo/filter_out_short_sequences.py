import os

from RNAFoldAssess.models import DataPointFromCrystal


rna_only_dir = "/common/yesselmanlab/ewhiting/data/crystal2/secondary_structures/rna_only/uniques"
w_protein_dir = "/common/yesselmanlab/ewhiting/data/crystal2/secondary_structures/with_protein/uniques"

r_dest = "/common/yesselmanlab/ewhiting/data/crystal2/secondary_structures/rna_only/preprocessed/twenty_plus"
p_dest = "/common/yesselmanlab/ewhiting/data/crystal2/secondary_structures/with_protein/preprocessed/twenty_plus"

rna_dps = DataPointFromCrystal.factory_from_dbn_files(rna_only_dir)
for dp in rna_dps:
    if len(dp.sequence) >= 20:
        cmd = f"cp {rna_only_dir}/{dp.name}.dbn {r_dest}/{dp.name}.dbn"
        os.system(cmd)

pro_dps = DataPointFromCrystal.factory_from_dbn_files(w_protein_dir)
for dp in pro_dps:
    if len(dp.sequence) >= 20:
        cmd = f"cp {w_protein_dir}/{dp.name}.dbn {p_dest }/{dp.name}.dbn"
        os.system(cmd)