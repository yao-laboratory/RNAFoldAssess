import os


chem_map_pred_map = {
    "EternaBench": "/mnt/nrdstor/yesselmanlab/ewhiting/reports/eterna_data/with_energy/canonical",
    "Ribonanza": "/mnt/nrdstor/yesselmanlab/ewhiting/reports/ribonanza/canonical",
    "RNAndria-miRNA": "/mnt/nrdstor/yesselmanlab/ewhiting/reports/rnandria/canonical",
    "RNAndria-mRNA": "/mnt/nrdstor/yesselmanlab/ewhiting/reports/rnandria/canonical",
    "YData": "/mnt/nrdstor/yesselmanlab/ewhiting/reports/ydata/canonize"
}

# n = 4178551
# Q1: 0.6974509803921569
# Median (Q2): 0.857397504456328
# Q3: 0.95

high_cutoff = 0.95
low_cutoff = 0.6974509803921569

def get_files(ds):
    loc = chem_map_pred_map[ds]
    if ds == "RNAndria-miRNA":
        files = [f for f in os.listdir(loc) if "miRNA" in f]
    elif ds == "RNAndria-mRNA":
        files = [f for f in os.listdir(loc) if "mRNA" in f]
    else:
        files = os.listdir(loc)
    
    return files
