import os

from RNAFoldAssess.utils import *

loc = "/common/yesselmanlab/ewhiting/reports/bprna/ContextFold_bpRNA-1m-90_report.txt"
model_name = "ContextFold"

analyze_bprna_evaluations(
    loc,
    model_name
)
