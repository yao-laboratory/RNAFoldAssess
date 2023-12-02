import os

from RNAFoldAssess.utils import *

loc = "/common/yesselmanlab/ewhiting/reports/bprna/IPknot_bpRNA-1m-90_report.txt"
model_name = "IPknot"

analyze_bprna_evaluations(
    loc,
    model_name
)
