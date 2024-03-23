import os, datetime

from RNAFoldAssess.utils import *
from RNAFoldAssess.models.predictors import *


model_name = "SeqFold"
model = SeqFold()
model_path = os.path.abspath("/home/yesselmanlab/ewhiting/.conda/envs/rna_fold_assess/bin/seqfold")

generate_ribonanza_evaluations(
    model,
    model_name,
    model_path,
    testing=False
)
