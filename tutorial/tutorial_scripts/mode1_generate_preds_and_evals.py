from RNAFoldAssess.models import DataPoint, PredictionPipeline
from RNAFoldAssess.models.predictors import *

"""
Mode 1 involves generating RNA secondary structure predictions from
one prediction model given a list of RNAs, and then evaluating the
prediction. This works with a collection of `DataPoint` objects.
"""

# Change this path to a JSON path containing your data
raw_data_path = "../processed_data/example_data_structure.csv"
# Change this path to where you want the predictions to be saved
output_path = "mode1_output.csv"

# Import the RNA data into a List of DataPoint objects
datapoints = DataPoint.init_from_csv_file(raw_data_path)

# Create a predictor object. If you have your own model, you can initialize it here.
rnaFold = RNAFold()

# We call the to_csv_file_with_prediction method on DataPoint
# to create a CSV file with the model's predictions and scores
PredictionPipeline.run_prediction(datapoints, rnaFold, output_path=output_path, prediction_mode=1)

# Now open the CSV file in the path recorded in the
# output_path variable to see the predictions.
