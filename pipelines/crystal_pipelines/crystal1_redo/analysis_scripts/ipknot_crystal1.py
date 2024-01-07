import os

from RNAFoldAssess.models import DataPointFromCrystal
from RNAFoldAssess.models.predictors import *
from RNAFoldAssess.utils import *

data_dir = "/common/yesselmanlab/ewhiting/data/crystal1_XRAY/redo_analysis/secondary_structures/preprocessed/twenty_plus"

model_name = "IPknot"
model = IPknot()
model_path = os.path.abspath("/common/yesselmanlab/ewhiting/ipknot-1.1.0-x86_64-linux/ipknot")
data_type_name = "crystal1"

crystal_evals(
    model=model,
    model_name=model_name,
    model_path=model_path,
    dbn_path=data_dir,
    data_type_name=data_type_name,
    testing=False
)
