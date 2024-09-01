import os, datetime, argparse

from RNAFoldAssess.utils import *
from RNAFoldAssess.models.predictors import *


model = MXFold2RetrainedRibonanza()
model_name = "MXFold2RetrainedRibonanza"

dp_path = "/common/yesselmanlab/ewhiting/data/translated_eterna_data/eterna.json"

partition_size = 8
parser = argparse.ArgumentParser()
parser.add_argument("--partition", help="Select 0 through 7 partition")
args = parser.parse_args()
partition = int(args.partition)

generate_eterna_data_evaluations_by_partition(
    model=model,
    model_name=model_name,
    model_path="",
    testing=False,
    partition_size=partition_size,
    partition_number=partition
)
