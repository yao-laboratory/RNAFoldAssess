from RNAFoldAssess.utils import *
from RNAFoldAssess.models.predictors import *

model_name = "RNAFold"
model = RNAFold()
model_path = os.path.abspath("/home/yesselmanlab/ewhiting/ViennaRNA/bin/RNAfold")

# predict_rasp_with_exons(model, model_name, model_path, species, make_seq_file=False)

predict_rasp_with_exons(
    model,
    model_name,
    model_path,
    "human"
)

