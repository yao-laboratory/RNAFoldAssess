import os

from models import *


# Testing with C009C
base_data_path = "/common/yesselmanlab/ewhiting/ss_deeplearning_data/data"
c009c = DataPoint.factory(f'{base_data_path}/C009C.json')
# For now, just use one data point from C009C
datum = c009c[0]
print(f"`dataum` class: {type(datum)}")
seq_file_path = datum.to_seq_file()

path_to_mxfold = "../mxfold/build/mxfold"
mxfold = MXFold()

fasta_file_path = os.path.abspath(datum.to_fasta_file())

mxfold.execute(path_to_mxfold, fasta_file_path)

mxfold_prediction = mxfold.get_ss_prediction()