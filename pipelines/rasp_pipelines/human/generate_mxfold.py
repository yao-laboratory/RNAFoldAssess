import os, datetime

from RNAFoldAssess.models import DataPointFromCrystal
from RNAFoldAssess.models.predictors import *
from RNAFoldAssess.utils import *

model_name = "MXFold"
model = MXFold()
model_path = os.path.abspath("/home/yesselmanlab/ewhiting/mxfold/build/mxfold")


species = "human"
data = f"/common/yesselmanlab/ewhiting/data/rasp_data/processed/{species}"

json_files = os.listdir(data)

for json_file in json_files:
    path = f"{data}/{json_file}"
    generate_rasp_data(
        model,
        model_name,
        model_path,
        path,
        "rasp",
        file_prefix=json_file.split(".")[0],
        species=species,
        testing=False,
        chemical_mapping_method="DMS"
    )


