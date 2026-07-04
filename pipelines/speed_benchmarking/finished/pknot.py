from RNAFoldAssess.utils import *
from RNAFoldAssess.models.predictors import *


model_name = "pKnots"
model = PKnots(use_scratch=True)
model_path = ""

benchmark_prediction_speed(
    model,
    model_name,
    model_path
)
