import os, datetime

from RNAFoldAssess.utils import *
from RNAFoldAssess.models.predictors import *


model = MXFold2RetrainedYData(remove_file_when_done=True)
model_name = "MXFold2RetrainedYData"

generate_ribonanza_evaluations(
    model,
    model_name,
    model_path,
    testing=False
)

