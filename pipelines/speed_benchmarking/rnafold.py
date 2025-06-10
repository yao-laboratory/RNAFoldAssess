from RNAFoldAssess.utils import *
from RNAFoldAssess.models.predictors import *


model = RNAFold()
model_name = "RNAFold"
model_path = os.path.abspath("/home/yesselmanlab/ewhiting/ViennaRNA/bin/RNAfold")

benchmark_prediction_speed(
    model,
    model_name,
    model_path
)