from RNAFoldAssess.utils import *
from RNAFoldAssess.models.predictors import *


model_name = "ContraFold"
model = ContraFold()
model_path = "/home/yesselmanlab/ewhiting/contrafold"

benchmark_prediction_speed(
    model,
    model_name,
    model_path
)
