import path

from models import *

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

print(f"Eterna Output: {eterna.output}")
print(f"Eterna Prediction: {eterna.get_ss_prediction()}")

eterna_prediction = Evaluator(datum, eterna.get_ss_prediction(), 'EternaFold')
print(f"Eterna evaluation: {eterna_prediction.metrics}")

# testing SPOT-RNA
path_to_spot_rna = path.Path("../SPOT-RNA").abspath()
fasta_file_path = datum.to_fasta_file()
spot = SPOT_RNA()
spot.execute(path_to_spot_rna, fasta_file_path)

print(f"SPOT-RNA Output: {spot.output}")
print(f"SPOT-RNA Prediction: {spot.get_ss_prediction()}")

spot_prediction = Evaluator(datum, spot.get_ss_prediction(), 'SPOT-RNA')
print(f"SPOT-RNA evaluation: {spot_prediction.metrics}")
