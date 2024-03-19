import os, datetime

from RNAFoldAssess.models.predictors import *
from RNAFoldAssess.utils import *


model_name = "MXFold"
model = MXFold()
model_path = os.path.abspath("/home/yesselmanlab/ewhiting/mxfold/build/mxfold")
data_type_name = "eterna_SHAPE"

print("Starting ...")
generate_eterna_data_evaluations(
    model,
    model_name,
    model_path,
    data_type_name=data_type_name,
    testing=False
)
print("Done")
