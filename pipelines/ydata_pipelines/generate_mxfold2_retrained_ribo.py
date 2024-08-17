import os, datetime
import sys

from RNAFoldAssess.models import DataPointFromCrystal
from RNAFoldAssess.models.predictors import *
from RNAFoldAssess.utils import *

model_name = "MXFold2RetrainedRibonanza"
model = MXFold2RetrainedRibonanza()
model_path = ""
data_type_name = "ydata"

args = sys.argv
cohort = args[1]

print(cohort)

print("starting ...")
generate_dms_evaluations_by_cohort(
    model=model,
    model_name=model_name,
    model_path=model_path,
    cohort=cohort,
    testing=False
)
print("done")