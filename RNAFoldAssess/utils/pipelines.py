from typing import List
import pandas as pd

from RNAFoldAssess.models import *


def predictions_from_model(model: Predictor, datapoints: List[DataPoint], save_csv_to="./predictions.csv"):
    fstring = "model_name,dp_name,sequence,ground_truth_type,ground_truth_data,prediction\n"
    for dp in datapoints:
        model.execute(dp)
        prediction = model.get_ss_prediction()
        fstring += f"{model},{dp.name},{dp.sequence},{dp.ground_truth_type},{dp.ground_truth_data},{prediction}\n"

    with open(save_csv_to, "w") as fh:
        fh.write(fstring.strip())
