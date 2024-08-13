import os

from RNAFoldAssess.models import DataPoint
from RNAFoldAssess.utils import ChemicalMappingTools, SecondaryStructureTools

ribo_data_csv = "/mnt/nrdstor/yesselmanlab/ewhiting/rna_data/ribonanza/rmdb_data.v1.3.0.csv"
f = open(ribo_data_csv)
data = f.readlines()
f.close()
# Get rid of headers
data.pop(0)
data = [d.split(",") for d in data]
r1_index = 7
# Experiment types:
# {'BzCN_cotx', 'deg_Mg_50C', 'BzCN', 'DMS_M2_seq', 'deg_pH10', 'deg_Mg_pH10', 'DMS_cotx', 'deg_50C', 'NMIA', 'DMS', 'CMCT', '1M7'
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

bpseq_dest = ""
counter = 0
len_data = len(data)
for d in data:
    counter += 1
    if counter % 357 == 0:
        print(f"Wokring {counter} of {len_data}")
    name = d[0]
    seq = d[1]
    experiment_type = d[2]
    chemical_mapping_method = experiment_map[experiment_type]
    reactivities = d[r1_index:len(seq) + r1_index]
    testable_reactivities = []
    for i, reactivity in enumerate(reactivities):
        if reactivity == "":
            testable_reactivities.append(-999)
        else:
            testable_reactivities.append(float(reactivity))

    dp = DataPoint({
        "name": name,
        "sequence": seq,
        "data": testable_reactivities,
        "reads": 0
    })

    ss_file = ChemicalMappingTools.generate_from_datapoint(dp, chemical_mapping_method)
    with open(ss_file) as sf:
        ss_data = sf.readlines()
    dbn = ss_data[2].strip()
    os.remove(ss_file)
    SecondaryStructureTools.write_bpseq_file(dp.name, dp.sequence, dbn, bpseq_dest)
