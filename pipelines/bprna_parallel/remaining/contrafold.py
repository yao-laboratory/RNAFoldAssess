import os

from RNAFoldAssess.models.predictors import *
from RNAFoldAssess.utils import *
from RNAFoldAssess.models.scorers import *


model_name = "ContraFold"
model = ContraFold()
model_path = os.path.abspath("/home/yesselmanlab/ewhiting/contrafold")


# Get leftovers
mismatch_file = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/bprna/mismatched_fasta_dbn_files.txt"
with open(mismatch_file) as f:
    mismatches = [d.strip() for d in f.readlines()]

prediction_file_name = "ContraFold_bpRNA-1m-90_all_report.txt"
pred_file_path = f"/mnt/nrdstor/yesselmanlab/ewhiting/reports/bprna/preprocessed/{prediction_file_name}"

with open(pred_file_path) as f:
    already_predicted = [d.split(", ")[1] for d in f.readlines()]

to_skip = mismatches + already_predicted

# Complete rest of predictions
sequence_data_path = "/work/yesselmanlab/ewhiting/data/bprna/fastaFiles"
dbn_data_path = "/work/yesselmanlab/ewhiting/data/bprna/dbnFiles"
mf = open("missing_fasta_files.txt", "a")

dbn_files = []
for df in os.listdir(dbn_data_path):
    if not df.startswith("bpRNA") and df.endswith(".dbn"):
        continue
    name = df.split(".")[0]
    if name not in to_skip: # I fucked this up, need to remove duplicates later
        dbn_files.append(df)

# report_file = open(pred_file_path, "a")
print("Starting")
lines_to_write = []
counter = 0
for df in dbn_files:
    counter += 1
    if counter % 25 == 0:
        report_file = open(pred_file_path, "a")
        report_file.writelines(lines_to_write)
        lines_to_write = []
    if counter % 750 == 0:
        print(f"Working {counter} of {len(dbn_files)}")
    name = df.split(".")[0]
    dbn_path = f"{dbn_data_path}/{df}"
    try:
        with open(dbn_path) as dfh:
            dbn_data = dfh.readlines()
            seq = dbn_data[3].strip()
            dbn = dbn_data[4].strip()

        if not sequence_is_only_nts(seq):
            print(f"{name}: sequence contains more than just ACUG nucleotides")
            continue

        dbn = dbn.replace("<", ".").replace(">", ".").replace("{", ".").replace("}", ".")

        seq_file_path = f"{sequence_data_path}/{name}.fasta"
        if not os.path.exists(seq_file_path):
            mf.write(f"{seq_file_path}\n")
            continue

        line_to_write = ""
        model.execute(model_path, seq_file_path)
        prediction = model.get_ss_prediction()
        for lenience in [0, 1]:
            line_to_write = f"{model_name}, {name}, {lenience}, "
            scorer = BasePairScorer(dbn, prediction, lenience)
            scorer.evaluate()
            s = scorer.sensitivity
            p = scorer.ppv
            f1 = scorer.f1
            line_to_write += f"{seq}, {dbn}, {prediction}, {s}, {p}, {f1}\n"
            lines_to_write.append(line_to_write)
    except Exception as e:
        print(f"Exception in file {seq_file_path}: {e}")
        continue


def sequence_is_only_nts(seq):
    nucleotides = {"A", "C", "U", "G", "a", "c", "u", "g"}
    seq_chars = set(seq)
    for sc in seq_chars:
        if sc not in nucleotides:
            return False
    return True

print("Done")

