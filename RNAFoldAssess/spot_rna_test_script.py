import os

from models import *


# Testing with C009C
base_data_path = "/common/yesselmanlab/ewhiting/ss_deeplearning_data/data"
c009c = DataPoint.factory(f'{base_data_path}/C009C.json')
# For now, just use one data point from C009C
datum = c009c[0]
print(datum.sequence)
fasta_file = datum.to_fasta_file()

spot_rna_path = os.path.abspath("../SPOT-RNA")
spot = SPOT_RNA()
spot.execute(spot_rna_path, fasta_file)

spot_prediction = spot.get_ss_prediction()

print(f"SPOT-RNA Output: {spot.output}")
print(f"SPOT-RNA Prediction: {spot_prediction}")


# Let's do this one by one
# spot_exec_string = f"python3 {spot_rna_path}/SPOT-RNA.py  --inputs {fasta_file}  --outputs ./spot_output"
# conda_exec_string = f"conda run -n spot {spot_exec_string}"
# print(f"Running: {conda_exec_string}\n")
# os.system(conda_exec_string)
# # Now use the .ct file to generate a dot-bracket string
# print("Create dot-bracket string from contact-table file")
# ct2db_path_string = "../ViennaRNA/src/Utils/ct2db"
# ct_file = fasta_file.split('/')[-1].replace('fasta', 'ct')
# ct_file_path = os.path.abspath(f"spot_output/{ct_file}")
# ct2db_exec_string = f"{ct2db_path_string} {str(ct_file_path)}"
# print(f"Running {ct2db_exec_string}\n")
# output = os.popen(ct2db_exec_string).read()
# print(f"Output: {output}\n")
