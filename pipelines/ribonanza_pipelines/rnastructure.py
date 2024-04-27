import os, datetime

from RNAFoldAssess.utils import *
from RNAFoldAssess.models.predictors import *


model_name = "RNAStructure"
model = RNAStructure()

generate_ribonanza_evaluations(
    model,
    model_name,
    "",
    to_seq_file=True,
    testing=False
)
