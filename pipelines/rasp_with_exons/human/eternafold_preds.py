from RNAFoldAssess.utils import *
from RNAFoldAssess.models.predictors import *

model_name = "EternaFold"
model = Eterna()
model_path = os.path.abspath("/home/yesselmanlab/ewhiting/EternaFold")


# predict_rasp_with_exons(model, model_name, model_path, species, make_seq_file=False)

predict_rasp_with_exons(
    model,
    model_name,
    model_path,
    "human",
    specific_chrs=["chr1"]
)

