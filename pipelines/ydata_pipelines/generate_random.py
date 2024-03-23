import os, datetime

from RNAFoldAssess.models import DataPointFromCrystal
from RNAFoldAssess.models.predictors import *
from RNAFoldAssess.utils import *

model_name = "RandomPredictor"
model = RandomPredictor()
data_type_name = "ydata"

print("starting ...")
generate_dms_evaluations(
    model=model,
    model_name=model_name,
    model_path="",
    testing=False
)
print("done")
