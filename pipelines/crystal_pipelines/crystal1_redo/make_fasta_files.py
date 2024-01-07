import os, datetime

from RNAFoldAssess.models import DataPointFromCrystal
from RNAFoldAssess.models.predictors import *
from RNAFoldAssess.models.scorers import *


destination_dir = "/common/yesselmanlab/ewhiting/data/crystal1_XRAY/fasta_files"
data_dir = "/common/yesselmanlab/ewhiting/data/crystal1_XRAY/redo_analysis/secondary_structures/preprocessed/twenty_plus"

data_points = DataPointFromCrystal.factory_from_dbn_files(data_dir)

len_dp = len(data_points)

print(f"Creating fasta files for {len_dp} data points")
counter = 0
for dp in data_points:
    if counter % 200 == 0:
        print(f"Generating file {counter} of {len_dp}")
    fasta_string = dp.to_fasta_string()
    f = open(f"{destination_dir}/{dp.name}.fasta", "w")
    f.write(fasta_string)
    f.close()
    counter += 1

