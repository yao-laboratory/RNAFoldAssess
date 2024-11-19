from RNAFoldAssess.utils import *
from RNAFoldAssess.models.predictors import *

model_name = "ContraFold"
model = ContraFold()
model_path = os.path.abspath("/home/yesselmanlab/ewhiting/contrafold")


# predict_rasp_with_exons(model, model_name, model_path, species, make_seq_file=False)

predict_rasp_with_exons(
    model,
    model_name,
    model_path,
    "ara-tha"
)
