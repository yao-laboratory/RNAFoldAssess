from RNAFoldAssess.utils import *
from RNAFoldAssess.models.predictors import *


model = ContextFold()
model_name = "ContextFold"
model_path = "/home/yesselmanlab/ewhiting/ContextFold_1_00"

benchmark_prediction_speed(
    model,
    model_name,
    model_path
)
