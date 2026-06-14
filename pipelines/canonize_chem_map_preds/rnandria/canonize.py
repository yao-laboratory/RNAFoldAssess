import os

from RNAFoldAssess.models import DataPoint
from RNAFoldAssess.models.scorers import *


existing_pred_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/rnandria"
dest_dir = f"{existing_pred_dir}/canonical"

models = [
    "ContextFold",
    "ContraFold",
    "EternaFold",
    "IPKnot",
    "NeuralFold",
    "NUPACK",
    "RNAFold",
    "RNAStructure",
    "pKnots",
    "Simfold",
    "MXFold",
    "MXFold2",
    "SPOT-RNA"
]

base_path = "/mnt/nrdstor/yesselmanlab/ewhiting/data/rnandria/rnandria_data_JSON/processed"
pri_miRNA = f"{base_path}/pri_miRNA_datapoints.json"
human_mRNA = f"{base_path}/human_mRNA_datapoints.json"

data_type_map = {"pri_miRNA": pri_miRNA, "human_mRNA": human_mRNA}

for data_type, json_file in data_type_map.items():
    print(f"Working {data_type}")
    dps = DataPoint.factory(json_file)
    # Make map
    dp_map = {}
    for dp in dps:
        dp_map[dp.name] = dp

    for m in models:
        print(f"\t{m}")
        fstring = ""
        pred_file = f"{existing_pred_dir}/{m}_rnandria_{data_type}_predictions.txt"
        with open(pred_file) as fh:
            pred_data = fh.readlines()

        if pred_data[0].startswith("algo"):
            pred_data.pop(0)

        pred_data = [pd.split(", ") for pd in pred_data]

        for pd in pred_data:
            dp_name = pd[1]
            sequence = pd[2]
            prediction = pd[3]
            dp = dp_map[dp_name]

            new_pred = CanonicalBasePairScorer.transform_structure(prediction, sequence)
            score = DSCI.score(
                sequence,
                new_pred,
                dp.reactivities,
                DMS=True
            )

            acc = score["accuracy"]
            p = score["p"]

            fstring += f"{m}, {dp_name}, {sequence}, {new_pred}, {acc}, {p}\n"

        with open(f"{dest_dir}/{m}_{data_type}_predictions.txt", "w") as fh:
            fh.write(fstring)


print("Done")
