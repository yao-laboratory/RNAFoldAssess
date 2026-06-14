import json

from RNAFoldAssess.models import DataPoint
from RNAFoldAssess.models.scorers import *


base_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/consolidated"
all_dps_file = f"{base_dir}/RASP_all_datapoints.csv"


def get_score(line, pred):
    dataset = line[0]
    chem_map_method = line[3]
    seq = line[2]
    ground_truth_data = line[4]
    ground_truth_data = eval(ground_truth_data)
    if type(ground_truth_data[0]) == list:
        ground_truth_type = "reactivity_map"
        score = score_reactivity_map(seq, pred, ground_truth_data, chem_map_method)
    else:
        ground_truth_type = "reactivities"
        score = score_reactivities(seq, pred, ground_truth_data, chem_map_method)
    return score


def score_reactivities(seq, pred, reactivities, chem_map_method):
    if chem_map_method == "DMS":
        score = DSCI.score(
            seq,
            pred,
            reactivities,
            DMS=True
        )
    else:
        score = DSCI.score(
            seq,
            pred,
            reactivities,
            SHAPE=True
        )

    return score

def score_reactivity_map(seq, pred, reactivity_map, chem_map_method):
    testable_seq = ""
    testable_pred = ""
    reactivities = []
    for pos, reactivity in reactivity_map:
        testable_seq += seq[pos]
        testable_pred += pred[pos]
        reactivities.append(reactivity)

    score = score_reactivities(testable_seq, testable_pred, reactivities, chem_map_method)

    return score


models = ["ContextFold", "ContraFold", "EternaFold", "IPKnot",
          "NeuralFold", "NUPACK", "RNAFold",
          "RNAStructure", "pKnots", "Simfold",
          "MXFold", "MXFold2", "SPOT-RNA"]

with open(all_dps_file) as fh:
    lines = fh.readlines()

lines = [line.split(";") for line in lines]
dp_line_map = {}
for line in lines:
    dp = line[1]
    dp_line_map[dp] = line


species = "ecoli"
with open(f"{base_dir}/RASP_{species}_canonical_preds_no_score.txt") as fh:
    pred_lines = [line.strip().split(", ") for line in fh.readlines()]

new_fstring = ""
counter = 0
tenths = len(pred_lines) // 10
for pl in pred_lines:
    counter += 1
    if counter % tenths == 0:
        print(f"Working {counter}")
    dp = pl[1]
    pred = pl[4]
    data_line = dp_line_map[dp]
    score = get_score(data_line, pred)
    acc = score["accuracy"]
    p = score["p"]
    new_line = ", ".join(pl) + f", {acc}, {p}\n"
    new_fstring += new_line

with open(f"{base_dir}/RASP_{species}_canonical_preds.txt", "w") as fh:
    fh.write(new_fstring)
