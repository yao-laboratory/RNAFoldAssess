import os


rna_only_dir = "/common/yesselmanlab/ewhiting/data/crystal2/fasta_files/rna_only"
w_protein_dir = "/common/yesselmanlab/ewhiting/data/crystal2/fasta_files/with_protein"


rna_files = [dbn[:4] for dbn in os.listdir(rna_only_dir) if dbn.endswith(".dbn")]
pro_files = [dbn[:4] for dbn in os.listdir(w_protein_dir) if dbn.endswith(".dbn")]

for pf in pro_files:
    if pf in rna_files:
        print(pf)

# Just to be super double sure
for rf in rna_files:
    if rf in pro_files:
        print(rf)

# None
