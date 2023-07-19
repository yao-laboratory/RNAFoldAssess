from models import *

# Testing with C009C
base_data_path = "../ss_deeplearning_data/data"
c009c = DataPoint.factory(f'{base_data_path}/C009C.json')
# For now, just use one data point from C009C
datum = c009c[0]
print(f"`dataum` class: {type(datum)}")
seq_file_path = datum.to_seq_file()

path_to_context_fold = "../ContextFold_1_00"
contextFold = ContextFold()

contextFold.execute(path_to_context_fold, datum.sequence)

cf_prediction = contextFold.get_ss_prediction()
print(f"ContextFold Output: {contextFold.output}")
print(f"ContextFold Prediction: {cf_prediction}")
