import os, datetime

from RNAFoldAssess.utils import *
from RNAFoldAssess.models.predictors import *


model_name = "RandomPredictor"
model = RandomPredictor()

generate_ribonanza_evaluations(
    model,
    model_name,
    "",
    testing=False
)
