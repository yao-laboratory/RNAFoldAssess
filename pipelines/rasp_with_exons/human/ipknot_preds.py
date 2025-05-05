from RNAFoldAssess.utils import *
from RNAFoldAssess.models.predictors import *

model_name = "IPKnot"
model = IPknot()
model_path = os.path.abspath("/common/yesselmanlab/ewhiting/ipknot-1.1.0-x86_64-linux/ipknot")


# predict_rasp_with_exons(model, model_name, model_path, species, make_seq_file=False)

predict_rasp_with_exons(
    model,
    model_name,
    model_path,
    "human",
    specific_chrs=["chr1", "chr18", "chr19"]
)

