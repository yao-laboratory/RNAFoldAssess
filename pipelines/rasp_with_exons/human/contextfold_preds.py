from RNAFoldAssess.utils import *
from RNAFoldAssess.models.predictors import *

model_name = "ContextFold"
model = ContextFold()
model_path = "/home/yesselmanlab/ewhiting/ContextFold_1_00"


# predict_rasp_with_exons(model, model_name, model_path, species, make_seq_file=False)

predict_rasp_with_exons(
    model,
    model_name,
    model_path,
    "human"
)

