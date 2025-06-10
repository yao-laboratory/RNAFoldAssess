from RNAFoldAssess.utils import *
from RNAFoldAssess.models.predictors import *


model_name = "RNAStructure"
model = RNAStructure()

benchmark_prediction_speed(
    model,
    model_name,
    ""
)
