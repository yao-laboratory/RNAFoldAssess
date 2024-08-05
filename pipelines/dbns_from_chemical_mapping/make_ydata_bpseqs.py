import os

from RNAFoldAssess.models import DataPoint
from RNAFoldAssess.utils import ChemicalMappingTools, SecondaryStructureTools


dp_file_path= "/common/yesselmanlab/ewhiting/ss_deeplearning_data/data"

approved_chorots = [
    "C014G",
    "C014H",
    "C014I",
    "C014J",
    "C014U",
    "C014V"
]

bpseq_dest = "/work/yesselmanlab/ewhiting/chem_map_to_bpseq/ydata/bpseq_files"

print("Assembling datapoints")
data_points = []
data_point_files = os.listdir(dp_file_path)
for dpf in data_point_files:
    cohort = dpf.split(".")[0]
    if cohort not in approved_chorots:
        continue
    print(f"Loading data points from {cohort} cohort")
    dps = DataPoint.factory(f"{dp_file_path}/{dpf}", cohort)
    for dp in dps:
        data_points.append(dp)

print("Done assembling datapoints")

print("Creating bpseq files")
len_data = len(data_points)
counter = 0
for dp in data_points:
    ss_file = ChemicalMappingTools.generate_from_datapoint(dp, "DMS")
    with open(ss_file) as sf:
        data = sf.readlines()
    dbn = data[2].strip()
    os.remove(ss_file)
    SecondaryStructureTools.write_bpseq_file(dp.name, dp.sequence, dbn, bpseq_dest)
    counter += 1
    if counter % 250 == 0:
        print(f"Working {counter} of {len_data}")
