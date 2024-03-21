import os, datetime

from RNAFoldAssess.utils import *
from RNAFoldAssess.models.predictors import *


model = ContextFold()
model_name = "ContextFold"
model_path = os.path.abspath("/home/yesselmanlab/ewhiting/ContextFold_1_00")

generate_ribonanza_evaluations(
    model,
    model_name,
    model_path,
    testing=False
)
