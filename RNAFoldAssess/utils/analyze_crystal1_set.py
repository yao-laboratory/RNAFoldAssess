from RNAFoldAssess.models import DataPointFromCrystal

crystal_base = "/common/yesselmanlab/ewhiting/data/crystal1_XRAY/symmetric_structures.txt"

dps = DataPointFromCrystal.factory(crystal_base)

# Experiment type for all of these is X-RAY


