import os

from RNAFoldAssess.models import DataPointFromCrystal


rna_only_dir = "/common/yesselmanlab/ewhiting/data/crystal2/secondary_structures/rna_only/uniques"
w_protein_dir = "/common/yesselmanlab/ewhiting/data/crystal2/secondary_structures/with_protein/uniques"

rna_only_destination = "/common/yesselmanlab/ewhiting/data/crystal2/fasta_files/rna_only"
w_protein_destination = "/common/yesselmanlab/ewhiting/data/crystal2/fasta_files/with_protein"

counter = 0
rna_dps = DataPointFromCrystal.factory_from_dbn_files(rna_only_dir)
len_rna_dp = len(rna_dps)
for rna_dp in rna_dps:
    if counter % 200 == 0:
        print(f"Generating file {counter} of {len_rna_dp}")
    fasta_string = rna_dp.to_fasta_string()
    f = open(f"{rna_only_destination}/{rna_dp.name}.fasta", "w")
    f.write(fasta_string)
    f.close()
    counter += 1


counter = 0
wp_dps = DataPointFromCrystal.factory_from_dbn_files(w_protein_dir)
len_wp_dp = len(wp_dps)
for wp_dp in wp_dps:
    if counter % 200 == 0:
        print(f"Generating file {counter} of {len_wp_dp}")
    fasta_string = wp_dp.to_fasta_string()
    f = open(f"{w_protein_destination}/{wp_dp.name}.fasta", "w")
    f.write(fasta_string)
    f.close()
    counter += 1


# Note to self.
# shared = ['1LU3', '3IZD', '4C4Q', '2Z9Q', '1C2W', '1C2X']
