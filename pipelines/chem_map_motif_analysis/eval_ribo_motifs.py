import json

from RNAFoldAssess.models.scorers import DSCI


models = {
    'EternaFold',
    'SPOT-RNA',
    'ContraFold',
    'pKnots',
    'NeuralFold',
    'NUPACK',
    'RNAStructure',
    'MXFold',
    'IPKnot',
    'RNAFold',
    'Simfold',
    'ContextFold',
    'MXFold2'
}

print("Loading data ...")
with open("/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions/ribo_motif_locs_and_reactivities.json") as fh:
    data = json.load(fh)


keys = list(data.keys())
k = keys[0]

# Example key:
# ETOBCR_VN1_0001_ANNOTATION_1
#
# data[k].keys() --> Models
#
# data[k]["NUPACK"] -->
"""
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
    }, ... etc ...
}
"""

def info_about_score(datapoint, motif, model, chem_mapping_data):
    _, seq, stc = motif.split("_")
    seq = seq.replace("&", "")
    stc = stc.replace("&", "")
    model_count = 0
    retval = {
        "accuracies": [],
        "p_values": [],
        "percent_of_positions": []
    }
    # Prediction data
    motif_pred_data = data[datapoint][model][motif]
    positions = motif_pred_data["positions"]
    testable_positions = motif_pred_data["testable_positions"]
    percent_of_positions = len(testable_positions) / len(positions)
    reactivities = motif_pred_data["testable_reactivities"]
    # Make index map of testable predictions
    position_map = {}
    for i, pos in enumerate(positions):
        position_map[pos] = i
    testable_seq = ""
    testable_stc = ""
    for testable_pos in testable_positions:
        index = position_map[testable_pos]
        testable_seq += seq[index]
        testable_stc += stc[index]

    try:
        if chem_mapping_data == "DMS":
            score = DSCI.score(
                testable_seq,
                testable_stc,
                reactivities,
                DMS=True
            )
        elif chem_mapping_data == "SHAPE":
            score = DSCI.score(
                testable_seq,
                testable_stc,
                reactivities,
                SHAPE=True
            )
        elif chem_map_data == "CMCT":
            score = DSCI.score(
                testable_seq,
                testable_stc,
                reactivities,
                CMCT=True
            )
        acc = score["accuracy"]
        p = score["p"]
        return (acc, p, percent_of_positions)
    except:
        return False


motif_data_map = {}
counter = 0
print("Analyzing data ...")
for dp in data:
    counter += 1
    if counter % 1000 == 0:
        print(f"Working {counter} of {len(data)}")
    if "chemical_mapping_method" in data[dp].keys():
        chemical_mapping_method = data[dp]["chemical_mapping_method"]
        for m in models:
            motifs = list(data[dp][m].keys())
            for motif in motifs:
                response = info_about_score(dp, motif, m, chemical_mapping_method)
                if not response:
                    continue
                acc, p, percent_of_positions = response
                try:
                    motif_data_map[motif]["accuracies"].append(acc)
                    motif_data_map[motif]["p_values"].append(p)
                    motif_data_map[motif]["percent_of_positions"].append(percent_of_positions)
                    motif_data_map[motif]["model_count"] += 1
                except KeyError:
                    motif_data_map[motif] = {
                        "accuracies": [acc],
                        "p_values": [p],
                        "percent_of_positions": [percent_of_positions],
                        "model_count": 1
                }
    else:
        continue

print("Writing data")
dest_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions"
with open(f"{dest_dir}/ribo_motif_data.json", "w") as fh:
    json.dump(motif_data_map, fh)

print("Done")
