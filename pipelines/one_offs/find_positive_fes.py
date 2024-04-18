import os


from RNAFoldAssess.utils.secondary_structure_tools import SecondaryStructureTools

weird_data = []
destination_dir = "/common/yesselmanlab/ewhiting/dataset_analyses/weird_data"
rasp_base = "/common/yesselmanlab/ewhiting/reports/rasp_data"

rasp_folders = [
    "arabidopsis",
    "covid",
    "ecoli",
    "HIV",
    "human"
]

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

all_folder_paths = []
for rf in rasp_folders:
    for m in models:
        all_folder_paths.append(f"{rasp_base}/{rf}/{m}/filtered")
        try:
            os.mkdir(f"{rasp_base}/{rf}/{m}/filtered/with_energies")
        except FileExistsError:
            continue


all_files = []
for fp in all_folder_paths:
    files = os.listdir(fp)
    files = [ff for ff in files if ff.endswith(".txt")]
    for f in files:
        data_file = open(f"{fp}/{f}")
        energy_file = open(f"{fp}/with_energies/{f}", "w")
        data = data_file.readlines()
        data_file.close()
        for d in data:
            items = d.split(", ")
            items = [i.strip() for i in items]
            seq = items[2]
            stc = items[3]
            fe = SecondaryStructureTools.get_free_energy(seq, stc)
            new_d = ", ".join(items) + f", {fe}\n"
            energy_file.write(new_d)
            if fe > 0:
                weird_data.append(new_d)
        energy_file.close()



newf = open(f"{destination_dir}/weird_rasp_mfe_data.txt", "w")
for d in weird_data:
    newf.write(d)

newf.close()
