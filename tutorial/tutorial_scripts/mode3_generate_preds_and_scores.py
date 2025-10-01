from RNAFoldAssess.models import DataPoint
from RNAFoldAssess.models.predictors import *
from RNAFoldAssess.utils import *

"""
Mode 2 involves generating RNA secondary structure predictions from
one prediction model given a list of RNAs, and then scoring the
prediction. This works with a collection of `DataPoint` objects.
"""

# Load the known data
raw_data_path = "../processed_data"
datapoints = DataPoint.init_from_csv_file(f"{raw_data_path}/example_data_structure.csv")

# Create a predictor object
rnaFold = RNAFold()

# We call the to_csv_file_with_prediction method on DataPoint
# to create a CSV file with the model's predictions and scores
PredictionPipeline.run_prediction(datapoints, rnaFold, output_path="mode3_output.csv", prediction_mode=3)

# Now open the CSV in generated_data/rna_fold_predictions.csv
# to see the predictions and prediction scores
