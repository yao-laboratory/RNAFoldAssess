from RNAFoldAssess.utils.secondary_structure_tools import SecondaryStructureTools


destination_dir = "/common/yesselmanlab/ewhiting/reports/rnandria/analyses/pri/redo"
hi_preds = "/common/yesselmanlab/ewhiting/reports/rnandria/analyses/pri/pri_miRNA_high_predictions.txt"

f = open(hi_preds)
data = f.readlines()
f.close()

data = [d.split(", ") for d in data]

new_data = []

for d in data:
    if d[1] == "SeqFold":
        continue
    seq = d[2]
    stc = d[3]
    fe = SecondaryStructureTools.get_free_energy(seq, stc)
    if fe < 0:
        print(d)

