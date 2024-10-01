import os, sys

from shared_functions import *
from RNAFoldAssess.models.predictors import *


partition = sys.argv[1]
model_name = "EternaFold"
model = Eterna()
model_path = os.path.abspath("/home/yesselmanlab/ewhiting/EternaFold")

dbn_path = f"/work/yesselmanlab/ewhiting/data/bprna/dbnFiles_sep/part_{partition}"
dbn_files = os.listdir(dbn_path)

headers = "model_name, dp_name, lenience, sequence, true_structure, predicted_structure, sensitivity, ppv, f1\n"

skipped = 0
report0 = open(report_path(model_name, 0, partition), "w")
report1 = open(report_path(model_name, 1, partition), "w")
report0.write(headers)
report1.write(headers)
reports = [report0, report1]

for df in dbn_files:
    try:
        seq_and_dbn = get_seq_and_dbn(f"{dbn_path}/{df}")
        if not seq_and_dbn:
            print(f"Problem with {partition}/{df}")
            skipped += 1
            continue
        else:
            dp_name = df.split(".")[0]
            seq, dbn = seq_and_dbn
            fasta_file = to_fasta_scratch(dp_name, seq)
            model.execute(model_path, fasta_file)
            prediction = model.get_ss_prediction()
            for lenience in [0, 1]:
                line = f"{model_name}, {dp_name}, {lenience}, {seq}, "
                line += pred_lines(dbn, prediction, lenience)
                reports[lenience].write(line)
    except Exception as e:
        print(f"Exception in {df}: {e}")
        skipped += 1
        continue

report0.close()
report1.close()

print(f"Done, skipped: {skipped}")
