import json

from rna_secstruct import SecStruct

from RNAFoldAssess.models.scorers import *


def get_sec_struct_object(seq, stc):
    try:
        return SecStruct(seq, stc)
    except:
        return False

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
matched_set_file = f"{base_dir}/chemical_mapping_matched_set.txt"

with open(matched_set_file) as fh:
    pred_data = [line.split(", ") for line in fh.readlines()]


ds_dp_motif_map = {}
for ds in datasets:
    ds_dp_motif_map[ds] = {}

print("Adding datapoints to datasets")
for pd in pred_data:
    ds = pd[0]
    dp = pd[2]
    if not dp in ds_dp_motif_map[ds].keys():
        ds_dp_motif_map[ds][dp] = {}
        for m in models:
            ds_dp_motif_map[ds][dp][m] = {}


counter = 0
for pd in pred_data:
    counter += 1
    if counter % 5000 == 0:
        print(f"Working {counter} of {len(pred_data)}")
    dataset = pd[0]
    model = pd[1]
    dp = pd[2]
    seq = pd[3]
    stc = pd[4]

    motif_data = get_sec_struct_object(seq, stc)
    if not motif_data:
        continue

    for k, v in motif_data.motifs.items():
        if len(v.sequence) <= 10:
            continue

        key = v.m_type + "_" + v.sequence + "_" + v.structure
        positions = v.positions
        ds_dp_motif_map[dataset][dp][model][key] = {"positions": positions}

"""Example
{
    "EternaData": {
        "ETOBCR_VN1_0001_ANNOTATION_1": {
            "ContraFold": {
                "HELIX_XXXX_(())": [1,2,34,35]
            },
            "ContextFold": {
                "SINGLESTRAND_XXXXX_.....": [30, 31, 32, 33, 34]
            }
        }
    }
}
"""

json_path = f"{base_dir}/predicted_motif_locations_chem_map.json"
with open(json_path, "w") as fh:
    json.dump(ds_dp_motif_map, fh)
