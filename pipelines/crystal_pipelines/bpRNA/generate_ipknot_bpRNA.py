import os, datetime

from RNAFoldAssess.models import DataPointFromCrystal
from RNAFoldAssess.models.predictors import *
from RNAFoldAssess.utils import *

model_name = "IPknot"
model = IPknot()
data_type_name = "bpRNA-1m-90"
model_path = os.path.abspath("/common/yesselmanlab/ewhiting/ipknot-1.1.0-x86_64-linux/ipknot")

print("starting ...")
generate_bpRNA_evaluations(
    model=model,
    model_name=model_name,
    model_path=model_path,
    testing=True
)
print("done")
