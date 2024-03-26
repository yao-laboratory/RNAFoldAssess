from RNAFoldAssess.utils.secondary_structure_tools import SecondaryStructureTools


lowest_quartile = 0.5985

base_dir = "/common/yesselmanlab/ewhiting/reports/ribonanza"

models = [
    "ContextFold",
    "ContraFold",
    "EternaFold",
    "IPKnot",
    "MXFold",
    "RandomPredictor",
    "RNAFold",
    "SeqFold"
]

chem_mapping_types = [
    "1M7",
    "BzCN_cotx",
    "BzCN",
    "CMCT",
    "deg_50C",
    "deg_Mg_50C",
    "deg_Mg_pH10",
    "deg_pH10",
    "DMS_cotx",
    "DMS_M2_seq",
    "DMS",
    "NMIA"
]

destination_dir = "/common/yesselmanlab/ewhiting/dataset_analyses/ribonanza"
good_guesses = open(f"{destination_dir}/Ribo_good_guesses.txt", "w")
bad_guesses = open(f"{destination_dir}/Ribo_bad_guesses.txt", "w")

for m in models:
    print(f"Working {m}")
    for cmt in chem_mapping_types:
        print(f"\t- {cmt}")
        file_path = f"{m}_{cmt}_predictions.txt"
        f = open(f"{base_dir}/{file_path}")
        data = f.readlines()
        f.close()
        if data == []:
            continue
        for d in data:
            d = d.strip()
            d = d.split(", ")
            seq = d[2]
            stc = d[3]
            acc = float(d[4])
            fe = SecondaryStructureTools.get_free_energy(seq, stc)
            if fe == "" or not fe:
                continue
            d = ", ".join(d)
            d += f", {fe}\n"
            if acc <= lowest_quartile:
                bad_guesses.write(d)
            else:
                good_guesses.write(d)


bad_guesses.close()
good_guesses.close()
