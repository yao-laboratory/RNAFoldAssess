import os

from RNAFoldAssess.models import DataPointFromCrystal
from RNAFoldAssess.models.predictors import *
from RNAFoldAssess.utils import *

data_dir = "/common/yesselmanlab/ewhiting/data/crystal1_XRAY/redo_analysis/secondary_structures/preprocessed/twenty_plus"

model_name = "RandomPredictor"
model = RandomPredictor()
data_type_name = "crystal1"

crystal_evals(
    model=model,
    model_name=model_name,
    model_path="",
    dbn_path=data_dir,
    data_type_name=data_type_name,
    testing=False
)
