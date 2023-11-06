import os, datetime


from RNAFoldAssess.models import DataPoint
from RNAFoldAssess.models.scorers import DSCI, DSCITypeError, DSCIValueError
from RNAFoldAssess.models.predictors import *
from RNAFoldAssess.utils import *

rna_fold = RNAFold()
rna_fold_path = os.path.abspath("/home/yesselmanlab/ewhiting/ViennaRNA/bin/RNAfold")

dp_path = "/common/yesselmanlab/ewhiting/ss_deeplearning_data/data"
data_points = get_data_point_list_from_directory(dp_path)

dp_size = len(data_points)
print(f"Total of {dp_size} data points")
print("Data points loaded!")

# for testing
# data_points = data_points[0:10000]

predictor_name = "RNAFold"
data_type = "DMS"

analysis_report_location = analysis_report_location(predictor_name, data_type)
f = open(analysis_report_location, "w")
print("Writing headers ...")
f.write(f"{headers}\n")

# For info on dataset later
lengths = []
accuracies = []
p_values = []

print("About to run evaluation ...")
counter = 0
lowest_acc = [None, 1.0]
highest_p = [None, 0.0]
skipped_count = 0
one_point_oh_accuracies = 0

for dp in data_points:
    if counter % 250 == 0:
      print(f"Completed {counter} of {dp_size}")
    lengths.append(len(dp.sequence))
    input_file_path = dp.to_fasta_file()
    rna_fold.execute(rna_fold_path, input_file_path)
    prediction = rna_fold.get_ss_prediction()
    try:
        score = DSCI.score(
            dp.sequence,
            prediction,
            dp.reactivities,
            DMS=True
        )
        accuracy = round(score["accuracy"], 4)
        p = round(score["p"], 4)

        accuracies.append(accuracy)
        p_values.append(p)

        if accuracy < lowest_acc[1]:
            lowest_acc = [dp.name, accuracy]

        if accuracy == 1.0:
            one_point_oh_accuracies += 1

        if p > highest_p[1]:
            highest_p = [dp.name, p]

        f.write(f"{predictor_name}, {dp.name}, {accuracy}, {p}, DMS\n")
        counter += 1
    except (DSCITypeError, DSCIValueError) as dsci_error:
        skipped_count += 1
        print(f"Encountered DSCI error on {dp.name}: {str(dsci_error)}")
        continue

f.close()

write_pipeline_report(predictor_name, data_type, lengths, accuracies, p_values, one_point_oh_accuracies, lowest_acc, highest_p, skipped_count)
