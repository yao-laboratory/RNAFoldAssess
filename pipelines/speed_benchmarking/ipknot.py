from RNAFoldAssess.utils import *
from RNAFoldAssess.models.predictors import *


model_name = "IPKnot"
model = IPknot()
model_path = os.path.abspath("/mnt/nrdstor/yesselmanlab/ewhiting/ipknot-1.1.0-x86_64-linux/ipknot")

benchmark_prediction_speed(
    model,
    model_name,
    model_path
)
