import os, datetime

from RNAFoldAssess.models import DataPointFromCrystal
from RNAFoldAssess.models.predictors import *
from RNAFoldAssess.utils import *

model_name = "RNAFold"
model = RNAFold()
model_path = os.path.abspath("/home/yesselmanlab/ewhiting/ViennaRNA/bin/RNAfold")
data_type_name = "ydata"

print("starting ...")
generate_dms_evaluations(
    model=model,
    model_name=model_name,
    model_path=model_path,
    testing=True
)
print("done")
