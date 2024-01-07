import os

from RNAFoldAssess.models import *

# I have no idea why this didn't work the first time around

fasta_path = "/common/yesselmanlab/ewhiting/data/crystal1_XRAY/fasta_files/"
dbn_path = "/common/yesselmanlab/ewhiting/data/crystal1_XRAY/redo_analysis/secondary_structures/preprocessed/twenty_plus/"

fasta_files = [fasta[:-6] for fasta in os.listdir(fasta_path) if fasta.endswith(".fasta")]
dbn_files = [dbn[:-4] for dbn in os.listdir(dbn_path) if dbn.endswith(".dbn")]

missing = set(dbn_files) - set(fasta_files)

# The list:
# 1YJW_8
# 5Z1I
# 1VQ9_9
# 2ZH2
# 1K73_9
# 2QA4_13
# 3G6E_8
# 7EOI
# 1N32_0
# 6DMD_1
# 4KR7_1
# 1QF6
# 4BW0
# 2GTT_1
# 7A0R_1
# 3CCV_8
# 3NVK_2
# 7EQJ_1
# 3D2X_0
# 6AAY_1

for m in missing:
    fpath = f"{dbn_path}/{m}.dbn"
    f = open(fpath)
    data = f.readlines()
    f.close()
    dp = DataPointFromCrystal(
        name = m,
        sequence = data[1].strip(),
        true_structure = data[2].strip()
    )
    fasta_string = dp.to_fasta_string()
    ff = open(f"{fasta_path}/{m}.fasta", "w")
    ff.write(fasta_string)
    ff.close()
