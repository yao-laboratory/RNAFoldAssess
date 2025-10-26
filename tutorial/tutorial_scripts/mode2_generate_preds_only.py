from RNAFoldAssess.models import DataPoint, PredictionPipeline
from RNAFoldAssess.models.predictors import *


"""
Mode 2 involves generating RNA secondary structure predictions from
one prediction model given a list of RNAs. This mode does not score
the secondary structure prediction, it only generates the prediction
given the RNA's sequence. Since it does not score the prediction,
there is no need for ground truth data in the CSV file. You can see
the CSV file in processed_data called example_data_no_ground_truth.csv
to see what such a file will look like. Once all predictions have been
generated, RNAFoldAssess writes them to a CSV file.
"""

# Change this path to a CSV file containing your own RNA sequences
raw_data_path = "../processed_data/example_data_no_ground_truth.csv"
# Chagne this path to where you want the predictions to be saved
output_path = "mode2_output.csv"

# Import the RNA data into a List of DataPoint objects
datapoints = DataPoint.init_from_csv_file(raw_data_path)

# Create a predictor object. If you have your own model, you can initialize it here.
rnaFold = RNAFold()

# Now we generate predictions only (no score)
# Default output path is ./predictions_no_score.csv
PredictionPipeline.run_prediction(dp_list=datapoints, model=rnaFold, output_path=output_path, prediction_mode=2)

# Now open the CSV file in the path recorded in the
# output_path variable to see the predictions.
