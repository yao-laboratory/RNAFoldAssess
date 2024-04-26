import os, datetime
import sys

from RNAFoldAssess.models import DataPointFromCrystal
from RNAFoldAssess.models.predictors import *
from RNAFoldAssess.utils import *

model_name = "MXFold2"
model = MXFold2()
model_path = ""
data_type_name = "ydata"

args = sys.argv
cohort = args[1]
partition = int(args[2])
partition_size = 8

print(cohort)

print("starting ...")
generate_dms_evaluations_by_cohort_partition(
    model=model,
    model_name=model_name,
    model_path=model_path,
    cohort=cohort,
    partition=partition,
    partition_size=partition_size,
    testing=False
)
print("done")


# U and V didn't finish
