from RNAFoldAssess.utils import *
from RNAFoldAssess.models.predictors import *


model = MXFold2()
model_name = "MXFold2"

benchmark_prediction_speed(
    model,
    model_name,
    ""
)
