from RNAFoldAssess.models import DataPoint
from RNAFoldAssess.models.predictors import *
from RNAFoldAssess.utils import *

"""
Mode 3 involves generating RNA secondary structure predictions from
one prediction model given a list of RNAs, and then scoring the
prediction. This works with a collection of `DataPoint` objects.
Note that in this script, we are using JSON represetnation of the
RNA objects, whereas in other examples, we used CSV.
"""

# Change this path to a JSON path containing your data
raw_data_path = "../processed_data/example_data.json"
# Change this path to where you want the predictions to be saved
output_path = "mode3_output.csv"

# Import the RNA data into a List of DataPoint objects
datapoints = DataPoint.init_from_csv_file(raw_data_path)

# Create a predictor object. If you have your own model, you can initialize it here.
rnaFold = RNAFold()

# We call the to_csv_file_with_prediction method on DataPoint
# to create a CSV file with the model's predictions and scores
PredictionPipeline.run_prediction(datapoints, rnaFold, output_path=output_path, prediction_mode=3)

# Now open the CSV file in the path recorded in the
# output_path variable to see the predictions.
