import os, datetime

from RNAFoldAssess.models import DataPointFromCrystal
from RNAFoldAssess.models.predictors import *
from RNAFoldAssess.utils import *

model_name = "MXFold"
model = MXFold()
model_path = os.path.abspath("/home/yesselmanlab/ewhiting/mxfold/build/mxfold")
data_type_name = "ydata"

print("starting ...")
generate_dms_evaluations(
    model=model,
    model_name=model_name,
    model_path=model_path,
    testing=True
)
print("done")
