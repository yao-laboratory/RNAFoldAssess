from RNAFoldAssess.models import DataPoint, PredictionPipeline
from RNAFoldAssess.models.predictors import *


"""
Mode 2 involves taking the CSV file of datapoints and their predictions
generated from Mode 1 and then scoring them.
"""
# Change this path to a CSV file containing your own RNA sequences
raw_data_path = "../processed_data/example_data_chem_mapping.csv"
# Change this path to the CSV file output by Mode 1
pred_only_csv_path = "mode1_output.csv"
# Chagne this path to where you want the predictions to be saved
output_path = "mode2_output.csv"

# Import the RNA data into a List of DataPoint objects
datapoints = DataPoint.init_from_csv_file(raw_data_path)

# Run in mode 2 to get score from previously generated predictions
PredictionPipeline.run_prediction(datapoints, output_path=output_path, input_path=pred_only_csv_path, prediction_mode=2)

# Now open the CSV file in the path recorded in the
# output_path variable to see the predictions.