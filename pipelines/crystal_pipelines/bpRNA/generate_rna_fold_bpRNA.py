import os, datetime, time

from RNAFoldAssess.models.predictors import *
from RNAFoldAssess.models.scorers import *
from RNAFoldAssess.utils import *

model_name = "RNAFold"
model = RNAFold()
model_path = os.path.abspath("/home/yesselmanlab/ewhiting/ViennaRNA/bin/RNAfold")
data_type_name = "bpRNA-1m-90"

print("starting ...")
generate_bpRNA_evaluations(
    model=model,
    model_name=model_name,
    model_path=model_path,
    testing=False
)
print("done")
