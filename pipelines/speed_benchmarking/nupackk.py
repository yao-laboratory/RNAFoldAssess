from RNAFoldAssess.utils import *
from RNAFoldAssess.models.predictors import *


model_name = "NUPACK"
model = NUPACK()

benchmark_prediction_speed(
    model,
    model_name,
    ""
)
