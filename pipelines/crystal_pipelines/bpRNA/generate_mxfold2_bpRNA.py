import os, datetime

from RNAFoldAssess.models import DataPointFromCrystal
from RNAFoldAssess.models.predictors import *
from RNAFoldAssess.utils import *

model_name = "MXFold2"
model = MXFold2()
model_path = ""
data_type_name = "bpRNA-1m-90"

print("starting ...")
generate_bpRNA_evaluations(
    model=model,
    model_name=model_name,
    model_path=model_path,
    sequence_data_path="/common/yesselmanlab/ewhiting/data/bprna/seq_files",
    testing=False
)
print("done")

