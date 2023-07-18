import path

from models import *

predictions = {}

# Testing with C009C
base_data_path = "../ss_deeplearning_data/data"
c009c = DataPoint.factory(f'{base_data_path}/C009C.json')
# For now, just use one data point from C009C
datum = c009c[0]
print(f"`dataum` class: {type(datum)}")
seq_file_path = datum.to_seq_file()

# Testing EternaFold
path_to_eternafold = path.Path("../EternaFold").abspath()
eterna = Eterna()
eterna.execute(path_to_eternafold, seq_file_path)

eterna_prediction = eterna.get_ss_prediction()

print(f"Eterna Output: {eterna.output}")
print(f"Eterna Prediction: {eterna_prediction}")

eterna_evaluation = Evaluator(datum, eterna.get_ss_prediction(), 'EternaFold')
eterna_metrics = eterna_evaluation.metrics
print(f"Eterna evaluation: {eterna_metrics}")
predictions['EternaFold'] = { 'prediction': eterna_prediction, 'evaluation': eterna_metrics }

# testing SPOT-RNA
path_to_spot_rna = path.Path("../SPOT-RNA").abspath()
fasta_file_path = datum.to_fasta_file()
spot = SPOT_RNA()
spot.execute(path_to_spot_rna, fasta_file_path)

spot_prediction = spot.get_ss_prediction()

print(f"SPOT-RNA Output: {spot.output}")
print(f"SPOT-RNA Prediction: {spot_prediction}")

spot_evaluation = Evaluator(datum, spot.get_ss_prediction(), 'SPOT-RNA').metrics
print(f"SPOT-RNA evaluation: {spot_evaluation}")
predictions['SPOT-RNA'] = { 'prediction': spot_prediction, 'evaluation': spot_evaluation }
