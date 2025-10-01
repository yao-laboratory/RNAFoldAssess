from RNAFoldAssess.models import DataPoint, PredictionPipeline
from RNAFoldAssess.models.predictors import *


"""
Mode 2 involves taking the CSV file of datapoints and their predictions
generated from Mode 1 and then scoring them.
"""

raw_data_path = "../processed_data"

# Import the RNA data into a List of DataPoint objects
datapoints = DataPoint.init_from_csv_file(f"{raw_data_path}/example_data_structure.csv")

# Get the path where the "prediction only" CSV is
pred_only_csv_path = "mode1_output.csv"

# Run in mode 2 to get score from previously generated predictions
PredictionPipeline.run_prediction(datapoints, output_path="mode2_output.csv", input_path=pred_only_csv_path, prediction_mode=2)
