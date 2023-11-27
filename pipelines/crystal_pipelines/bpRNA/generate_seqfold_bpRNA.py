import os, datetime

from RNAFoldAssess.models import DataPointFromCrystal
from RNAFoldAssess.models.predictors import *
from RNAFoldAssess.utils import *

model_name = "SeqFold"
model = SeqFold()
model_path = os.path.abspath("/home/yesselmanlab/ewhiting/.conda/envs/rna_fold_assess/bin/seqfold")
data_type_name = "bpRNA-1m-90"

print("starting ...")
generate_bpRNA_evaluations(
    model=model,
    model_name=model_name,
    model_path=model_path,
    testing=True
)
print("done")
