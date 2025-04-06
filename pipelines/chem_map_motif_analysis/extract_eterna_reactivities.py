import json

from RNAFoldAssess.models import DataPoint, EternaDataPoint


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
eterna_data = data["EternaData"]

data_points_path="/common/yesselmanlab/ewhiting/data/translated_eterna_data/eterna.json"
datapoints = EternaDataPoint.factory(data_points_path)

print(f"Working ...")
counter = 0
for dp in datapoints:
    counter += 1
    if counter % 10000 == 0:
        print(f"Working {counter} of {len(datapoints)}")
    if dp.name not in eterna_data:
        continue
    new_data[dp.name] = {}
    dp_pred_data = eterna_data[dp.name]
    for model, motif_data in dp_pred_data.items():
        new_data[dp.name][model] = {}
        for motif, motif_data in motif_data.items():
            new_data[dp.name][model][motif] = {}
            try:
                motif_positions = motif_data["positions"]
                new_data[dp.name][model][motif]["positions"] = motif_positions
                new_data[dp.name]["chemical_mapping_method"] = dp.mapping_method
                positions_with_chem_map_data = dp.positions
                testable_positions = [i for i in positions_with_chem_map_data if i in motif_positions]
                new_data[dp.name][model][motif]["testable_positions"] = testable_positions
                reactivities_index = [dp.reactivities_index[p] for p in testable_positions]
                reactivities = [dp.reactivities[i] for i in reactivities_index]
                new_data[dp.name][model][motif]["testable_reactivities"] = reactivities
            except IndexError:
                breakpoint()


json_dest = f"{base_dir}/eterna_motif_locs_and_reactivities.json"
with open(json_dest, "w") as fh:
    json.dump(new_data, fh)

print("Done")

"""
key: "NUPACK"
{
    'HELIX_UAUUCUAAG&CUUAGAGUA_(((((((((&)))))))))': {
        'positions': [5, 6, 7, 8, 9, 10, 11, 12, 13, 76, 77, 78, 79, 80, 81, 82, 83, 84],
        'testable_positions': [9, 10, 11, 12, 13],
        'testable_reactivities': [0.0, 0.042065, 0.028083, 0.030784, 0.037492]
    },
    'JUNCTION_GC&GG&CG&CC_((&)(&)(&))': {
        'positions': [13, 14, 33, 34, 55, 56, 75, 76],
        'testable_positions': [13, 14, 33, 34, 55, 56, 75],
        'testable_reactivities': [0.037492, 0.010798, 0.01997, 0.011467, 0.0, 1.0, 0.113255]
    },
    'HELIX_CGAUGGUG&UACUAUUG_((((((((&))))))))': {
        'positions': [14, 15, 16, 17, 18, 19, 20, 21, 26, 27, 28, 29, 30, 31, 32, 33],
        'testable_positions': [14, 15, 16, 17, 18, 19, 20, 21, 26, 27, 28, 29, 30, 31, 32, 33],
        'testable_reactivities': [0.010798, 0.026931, 0.042065, 0.056479, 0.037136, 0.047612, 0.030573, 0.026609, 0.012348, 0.015151, 0.018428, 0.015642, 0.046257, 0.03302, 0.030624, 0.01997]
    },
    'HELIX_GUGUUGAU&AUCAACAC_((((((((&))))))))': {
        ...
"""
