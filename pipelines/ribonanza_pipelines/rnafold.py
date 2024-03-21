import os, datetime

from RNAFoldAssess.utils import *
from RNAFoldAssess.models.predictors import *


model_name = "RNAFold"
model = RNAFold()
model_path = os.path.abspath("/home/yesselmanlab/ewhiting/ViennaRNA/bin/RNAfold")

generate_ribonanza_evaluations(
    model,
    model_name,
    model_path,
    testing=False
)
