import os, datetime

from RNAFoldAssess.utils import *
from RNAFoldAssess.models.predictors import *


model_name = "CFRetrainedEterna"
model = CFRetrainedEterna()
model_path = model_path = "/home/yesselmanlab/ewhiting/contrafold"

generate_ribonanza_evaluations(
    model,
    model_name,
    model_path,
    to_seq_file=True,
    testing=False
)
