import os, datetime

from RNAFoldAssess.utils import *
from RNAFoldAssess.models.predictors import *


model_name = "NUPACK"
model = NUPACK()
model_path = ""

generate_ribonanza_evaluations(
    model,
    model_name,
    model_path,
    testing=False
)
