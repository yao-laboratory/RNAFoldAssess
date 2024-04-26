import os, datetime


from RNAFoldAssess.utils import *
from RNAFoldAssess.models.predictors import *

model_name = "RNAStructure"
model = RNAStructure()

dp_path = "/common/yesselmanlab/ewhiting/data/translated_eterna_data/eterna.json"


generate_eterna_data_evaluations(
    model=model,
    model_name=model_name,
    model_path="",
    to_seq_file=True,
    testing=False
)
