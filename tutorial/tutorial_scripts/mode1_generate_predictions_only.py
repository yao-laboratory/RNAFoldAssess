from RNAFoldAssess.models import DataPoint, PredictionPipeline
from RNAFoldAssess.models.predictors import *


"""
Mode 1 involves generating RNA secondary structure predictions from
one prediction model given a list of RNAs. This mode does not score
the secondary structure prediction, it only generates the prediction
given the RNA's sequence. Once all predictions have been generated,
RNAFoldAssess writes them to a CSV file.
"""

raw_data_path = "../processed_data"

# Import the RNA data into a List of DataPoint objects
datapoints = DataPoint.init_from_csv_file(f"{raw_data_path}/example_data_structure.csv")

# Create a predictor object
rnaFold = RNAFold()

# Now we generate predictions only (no score)
# Default output path is ./predictions_no_score.csv
PredictionPipeline.run_prediction(dp_list=datapoints, model=rnaFold, output_path="mode1_output.csv")

# Now open the CSV file in this directory called
# predictions_no_score.csv to see the structure predictions
