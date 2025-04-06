from RNAFoldAssess.utils import *
from RNAFoldAssess.models.predictors import *


model_name = "MXFold"
model = MXFold()
model_path = os.path.abspath("/home/yesselmanlab/ewhiting/mxfold/build/mxfold")

# predict_rasp_with_exons(model, model_name, model_path, species, make_seq_file=False)

predict_rasp_with_exons(
    model,
    model_name,
    model_path,
    "ara-tha"
)
