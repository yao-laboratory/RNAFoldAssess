import os, datetime

from RNAFoldAssess.utils import *
from RNAFoldAssess.models.predictors import *



model_name = "SeqFold"
model = SeqFold()
model_path = os.path.abspath("/home/yesselmanlab/ewhiting/.conda/envs/rna_fold_assess/bin/seqfold")

base_path = "/common/yesselmanlab/ewhiting/data/rnandria/rnandria_data_JSON/processed"
pri_miRNA = f"{base_path}/pri_miRNA_datapoints.json"
human_mRNA = f"{base_path}/human_mRNA_datapoints.json"

generate_rnandria_evaluations(
    model,
    model_name,
    model_path,
    pri_miRNA,
    "pri_miRNA",
    testing=False
)

generate_rnandria_evaluations(
    model,
    model_name,
    model_path,
    human_mRNA,
    "human_mRNA",
    testing=False
)