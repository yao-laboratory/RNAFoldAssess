import os, datetime

from RNAFoldAssess.models import DataPointFromCrystal
from RNAFoldAssess.models.predictors import *
from RNAFoldAssess.utils import *


model_name = "RandomPredictor"
model = RandomPredictor()
model_path = ""

species_experiment = [
  ("arabidopsis", "DMS"),
  ("covid", "SHAPE"),
  ("ecoli", "DMS"),
  ("HIV", "SHAPE"),
  ("human", "DMS")
]

for species, experiment_type in species_experiment:
    data = f"/common/yesselmanlab/ewhiting/data/rasp_data/processed/{species}"
    json_files = os.listdir(data)
    print(f"Starting {model_name} - {species}")
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
            chemical_mapping_method=experiment_type
        )
