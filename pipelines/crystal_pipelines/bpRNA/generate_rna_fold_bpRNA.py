import os, datetime, time

from RNAFoldAssess.models.predictors import *
from RNAFoldAssess.models.scorers import *

model_name = "RNAFold"
model = RNAFold()
model_path = os.path.abspath("/home/yesselmanlab/ewhiting/ViennaRNA/bin/RNAfold")
data_type_name = "bpRNA-1m-90"
headers = "algo_name, datapoint_name, lenience, sensitivity, ppv, F1, data_point_type"
leniences = []
skipped = 0

analysis_report_path = f"/common/yesselmanlab/ewhiting/reports/{model_name}_{data_type_name}_report.txt"

counter = 0
dbn_path = "/common/yesselmanlab/ewhiting/data/bprna/dbnFiles"
fasta_path = "/common/yesselmanlab/ewhiting/data/bprna/fasta_files"
fasta_files = os.listdir(fasta_path)

leniences = [0, 1]

f = open(analysis_report_path, "w")
f.write(f"{headers}\n")
f.close()
file_len = len(fasta_files)
# For testing:
# fasta_files = fasta_files[0:500]

start = time.time()

rows_to_write = []
for fasta_file in fasta_files:
    if counter % 100 == 0:
        print(f"Writing {counter} of {file_len}")
        f = open(analysis_report_path, "a")
        for r in rows_to_write:
            f.write(r)
        f.close()
        rows_to_write = []
    name = fasta_file.split(".")[0]
    data_type = name.split("_")[1]
    dbn_file_path = f"{dbn_path}/{name}.dbn"
    # e.g. bpRNA_CRW_49455.dbn
    dbn_file = open(dbn_file_path)
    data = dbn_file.readlines()
    true_structure = data[4].strip()
    dbn_file.close()
    try:
        line_to_write = ""
        model.execute(model_path, f"{fasta_path}/{fasta_file}", delete_input_file_immediately=False)
        prediction = model.get_ss_prediction()
        for lenience in leniences:
            line_to_write = f"{model_name}, {name}, {lenience}, "
            scorer = BasePairScorer(true_structure, prediction, lenience)
            scorer.evaluate()
            s = scorer.sensitivity
            p = scorer.ppv
            f1 = scorer.f1

            line_to_write += f"{s}, {p}, {f1}\n"
            rows_to_write.append(line_to_write)
        counter += 1
    except:
        skipped += 1
        continue

if len(rows_to_write) != 0:
    print(f"Writing {counter} of {file_len}")
    f = open(analysis_report_path, "a")
    for r in rows_to_write:
        f.write(r)
    f.close()
    rows_to_write = []

end = time.time()
elapsed = end - start

print(f"From {len(fasta_files)}, this took {elapsed} seconds")
projected_time = (file_len / elapsed) / 60 / 60
print(f"Projected time to do every data point: {projected_time} hours")
