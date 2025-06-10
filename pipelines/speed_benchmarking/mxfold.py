from RNAFoldAssess.utils import *
from RNAFoldAssess.models.predictors import *


model = MXFold()
model_name = "MXFold"
model_path = os.path.abspath("/home/yesselmanlab/ewhiting/mxfold/build/mxfold")

benchmark_prediction_speed(
    model,
    model_name,
    model_path
)
