import os, datetime, time

from RNAFoldAssess.models import DataPointFromCrystal
from RNAFoldAssess.models.predictors import *
from RNAFoldAssess.utils import *


model_name = "ContextFold"
model = ContextFold()
model_path = os.path.abspath("/home/yesselmanlab/ewhiting/ContextFold_1_00")
data_type_name = "ydata"

print("starting ...")
generate_dms_evaluations(
    model=model,
    model_name=model_name,
    model_path=model_path,
    testing=True
)
print("done")
