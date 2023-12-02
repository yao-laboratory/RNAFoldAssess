import os

from RNAFoldAssess.utils import *

loc = "/common/yesselmanlab/ewhiting/reports/bprna/EternaFold_bpRNA-1m-90_report.txt"
model_name = "EternaFold"

analyze_bprna_evaluations(
    loc,
    model_name
)
