import json

from RNAFoldAssess.models import DataPoint


datasets = {
    'EternaData',
    'Ribonanza',
    'YesselmanLab',
    'RNAndria'
}

models = {
    'ContraFold',
    'NeuralFold',
    'EternaFold',
    'NUPACK',
    'pKnots',
    'ContextFold',
    'RNAFold',
    'SPOT-RNA',
    'MXFold',
    'MXFold2',
    'Simfold',
    'IPKnot',
    'RNAStructure'
}

base_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions"
json_path = f"{base_dir}/predicted_motif_locations_chem_map.json"

with open(json_path) as fh:
    data = json.load(fh)

"""Example
data["EternaData"]["ETOBCR_VN1_0001_ANNOTATION_1"]
{
    'NUPACK': {
        'HELIX_UAUUCUAAG&CUUAGAGUA_(((((((((&)))))))))':{
            'positions': [5, 6, 7, 8, 9, 10, 11, 12, 13, 76, 77, 78, 79, 80, 81, 82, 83, 84]
        },
        'JUNCTION_GC&GG&CG&CC_((&)(&)(&))': {
            'positions': [13, 14, 33, 34, 55, 56, 75, 76]
        },
        'HELIX_CGAUGGUG&UACUAUUG_((((((((&))))))))': {
            'positions': [14, 15, 16, 17, 18, 19, 20, 21, 26, 27, 28, 29, 30, 31, 32, 33]
        },
        'HELIX_GUGUUGAU&AUCAACAC_((((((((&))))))))': {
            'positions': [56, 57, 58, 59, 60, 61, 62, 63, 68, 69, 70, 71, 72, 73, 74, 75]
        },
        'SINGLESTRAND_AAAGAAACAACAACAACAAC_....................': {
            'positions': [85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104]
        }
    },
    'RNAFold': {
        'HELIX_UAUUCUAAG&CUUAGAGUA_(((((((((&)))))))))': {
            'positions': [5, 6, 7, 8, 9, 10, 11, 12, 13, 76, 77, 78, 79, 80, 81, 82, 83, 84]
        }, etc..
}
"""

new_data = {}
ydata = data["YesselmanLab"]

base_dp_path = "/common/yesselmanlab/ewhiting/ss_deeplearning_data/data"
cohorts = [
    "C014G",
    "C014H",
    "C014I",
    "C014J",
    "C014U",
    "C014V"
]

datapoints = []

for cohort in cohorts:
    json_path = f"{base_dp_path}/{cohort}.json"
    datapoints += DataPoint.factory(json_path, cohort)


print(f"Working ...")
counter = 0
for dp in datapoints:
    counter += 1
    if counter % 10000 == 0:
        print(f"Working {counter} of {len(datapoints)}")
    if dp.name not in ydata:
        continue
    new_data[dp.name] = {}
    dp_pred_data = ydata[dp.name]
    for model, motif_data in dp_pred_data.items():
        new_data[dp.name][model] = {}
        for motif, motif_data in motif_data.items():
            new_data[dp.name][model][motif] = {}
            try:
                motif_positions = motif_data["positions"]
                new_data[dp.name][model][motif]["positions"] = motif_positions
                new_data[dp.name]["chemical_mapping_method"] = "DMS"
                testable_positions = [i for i in motif_positions]
                new_data[dp.name][model][motif]["testable_positions"] = motif_positions
                new_data[dp.name][model][motif]["testable_reactivities"] = dp.reactivities
            except IndexError:
                breakpoint()

json_dest = f"{base_dir}/ydata_motif_locs_and_reactivities.json"
with open(json_dest, "w") as fh:
    json.dump(new_data, fh)

print("Done")
