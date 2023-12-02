import os

from RNAFoldAssess.utils import *

loc = "/common/yesselmanlab/ewhiting/reports/bprna/MXFold_bpRNA-1m-90_report.txt"
model_name = "MXFold"

analyze_bprna_evaluations(
    loc,
    model_name
)
