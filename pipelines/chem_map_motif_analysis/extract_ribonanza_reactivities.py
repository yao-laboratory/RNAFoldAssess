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
ribo_data = data["Ribonanza"]


ribo_data_csv = "/mnt/nrdstor/yesselmanlab/ewhiting/rna_data/ribonanza/rmdb_data.v1.3.0.csv"
with open(ribo_data_csv) as fh:
    data = fh.readlines()

data.pop(0)
data = [d.split(",") for d in data]
r1_index = 7
experiment_map = {
    "BzCN_cotx": "DMS4",
    "DMS_M2_seq": "DMS4",
    "DMS_cotx": "DMS4",
    "DMS": "DMS4",
    "1M7": "SHAPE",
    "NMIA": "SHAPE",
    "BzCN": "SHAPE",
    "deg_Mg_50C": "SHAPE",
    "deg_50C": "SHAPE",
    "deg_pH10": "SHAPE",
    "deg_Mg_pH10": "SHAPE",
    "CMCT": "CMCT"
}

datapoints = []
for d in data:
    name = d[0]
    if name not in ribo_data:
        continue
    seq = d[1]
    experiment_type = d[2]
    chemical_mapping_method = experiment_map[experiment_type]
    reactivities = d[r1_index:len(seq) + r1_index]
    testable_seq = ""
    testable_reactivities = []
    positions = []
    for i, reactivity in enumerate(reactivities):
        if reactivity != "":
            positions.append(i)
            testable_seq += seq[i]
            testable_reactivities.append(float(reactivity))

    # Using EternaDataPoint model because it's more appropriate
    data_hash = {
        "name": name,
        "sequence": seq,
        "mapping_method": chemical_mapping_method,
        "positions": positions,
        "reactivities": testable_reactivities
    }
    datapoint = EternaDataPoint(data_hash, normalize_reactivities_on_init=False)
    datapoints.append(datapoint)


print(f"Working ...")
counter = 0
for dp in datapoints:
    counter += 1
    if counter % 10000 == 0:
        print(f"Working {counter} of {len(datapoints)}")
    if dp.name not in ribo_data:
        continue
    new_data[dp.name] = {}
    dp_pred_data = ribo_data[dp.name]
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


json_dest = f"{base_dir}/ribo_motif_locs_and_reactivities.json"
with open(json_dest, "w") as fh:
    json.dump(new_data, fh)

print("Done")
