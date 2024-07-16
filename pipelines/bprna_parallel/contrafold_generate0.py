from RNAFoldAssess.models.predictors import *
from RNAFoldAssess.utils import *

model_name = "ContraFold"
model = ContraFold()
model_path = os.path.abspath("/home/yesselmanlab/ewhiting/EternaFold")

parallel_bprna_predictions(
    model,
    model_name,
    model_path,
    0,
    testing=True
)
