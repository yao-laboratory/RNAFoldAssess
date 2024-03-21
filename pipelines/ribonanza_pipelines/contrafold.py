import os, datetime

from RNAFoldAssess.utils import *
from RNAFoldAssess.models.predictors import *


model_name = "ContraFold"
model = ContraFold()
model_path = os.path.abspath("/home/yesselmanlab/ewhiting/EternaFold")

generate_ribonanza_evaluations(
    model,
    model_name,
    model_path,
    to_seq_file=True,
    testing=False
)
