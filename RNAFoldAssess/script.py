# Old and obsolete, delete later


import path

from models import *

predictions = {}

# Testing with C009C
base_data_path = "/common/yesselmanlab/ewhiting/ss_deeplearning_data/data"
c009c = DataPoint.factory(f'{base_data_path}/C009C.json')
# For now, just use one data point from C009C
datum = c009c[0]
print(f"`dataum` class: {type(datum)}")
seq_file_path = datum.to_seq_file()

# Testing EternaFold
path_to_eternafold = path.Path("../../EternaFold").abspath()
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

# testing ContextFold
path_to_context_fold = "../ContextFold_1_00"
contextFold = ContextFold()

contextFold.execute(path_to_context_fold, datum.sequence)

cf_prediction = contextFold.get_ss_prediction()
print(f"ContextFold Output: {contextFold.output}")
print(f"ContextFold Prediction: {cf_prediction}")

cf_evaluation = Evaluator(datum, cf_prediction, 'ContextFold').metrics
print(f"ContextFold evaluation: {cf_evaluation}")
predictions['ContextFold'] = { 'prediction': cf_prediction, 'evaluation': cf_evaluation }

# testing MXFold
path_to_mxfold = "../mxfold/build/mxfold"
mxfold = MXFold()

mxfold.execute(path_to_mxfold, fasta_file_path)

mxfold_prediction = mxfold.get_ss_prediction()
print(f"MXFold Output: {mxfold.output}")
print(f"MXFold Prediction: {mxfold_prediction}")

mxfold_evaluation = Evaluator(datum, mxfold_prediction, 'MXFold').metrics
print(f"MXFold evaluation: {mxfold_evaluation}")
predictions['MXFold'] = { 'prediction': mxfold_prediction, 'evaluation': mxfold_evaluation }


# Display predictions
for k in predictions:
  acc = predictions[k]['evaluation']['accuracy']
  p = predictions[k]['evaluation']['p']
  tab_size = 1
  if len(k) < 8:
    tab_size = 2
  tabs = "\t" * tab_size
  print(f"{k + tabs}- Accuracy: {round(acc, 5)}, p value: {round(p, 5)}")

