from RNAFoldAssess.utils import *
from RNAFoldAssess.models.predictors import *


model_name = "MXFold2"
model = MXFold2()

# predict_rasp_with_exons(model, model_name, model_path, species, make_seq_file=False)

predict_rasp_with_exons(
    model,
    model_name,
    "",
    "ara-tha"
)
