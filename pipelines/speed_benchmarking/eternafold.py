from RNAFoldAssess.utils import *
from RNAFoldAssess.models.predictors import *


model_name = "EternaFold"
model = Eterna()
model_path = os.path.abspath("/home/yesselmanlab/ewhiting/EternaFold")

benchmark_prediction_speed(
    model,
    model_name,
    model_path
)
