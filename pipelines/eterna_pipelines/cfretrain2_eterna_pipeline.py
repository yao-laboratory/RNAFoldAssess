import os, datetime


from RNAFoldAssess.utils import *
from RNAFoldAssess.models.predictors import *

model_name = "ContraRetrained2"

model = ContraRetrained2()
model_path = os.path.abspath("/home/yesselmanlab/ewhiting/EternaFold")

dp_path = "/common/yesselmanlab/ewhiting/data/translated_eterna_data/eterna.json"

generate_eterna_data_evaluations(
    model=model,
    model_name=model_name,
    model_path=model_path,
    testing=False
)
