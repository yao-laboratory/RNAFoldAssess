import os, datetime

from RNAFoldAssess.utils import *
from RNAFoldAssess.models.predictors import *


model = MXFold2RetrainedRNAndria()
model_name = "MXFold2RetrainedRNAndria"
model_path = ""

generate_ribonanza_evaluations(
    model,
    model_name,
    model_path,
    testing=False
)

