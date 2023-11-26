import os, datetime, time

from RNAFoldAssess.models import DataPointFromCrystal
from RNAFoldAssess.models.predictors import *
from RNAFoldAssess.models.scorers import *


model_name = "ContextFold"
model = ContextFold()
model_path = os.path.abspath("/home/yesselmanlab/ewhiting/ContextFold_1_00")
data_type_name = "bpRNA-1m-90"


def generate_c_bpRNA_evaluations(model,
                               model_name,
                               model_path,
                               sequence_data_path="/common/yesselmanlab/ewhiting/data/bprna/fasta_files",
                               leniences=[0, 1],
                               testing=False):
    data_type_name = "bpRNA-1m-90"
    headers = "algo_name, datapoint_name, lenience, sensitivity, ppv, F1, data_point_type"
    skipped = 0
    lengths = []
    weird_sequences = []
    analysis_report_path = f"/common/yesselmanlab/ewhiting/reports/bprna/{model_name}_{data_type_name}_report.txt"
    # Make the file
    f = open(analysis_report_path, "w")
    f.close()
    aux_data_path = f"/common/yesselmanlab/ewhiting/reports/bprna/{model_name}_{data_type_name}_aux_data.txt"
    counter = 0
    dbn_path = "/common/yesselmanlab/ewhiting/data/bprna/dbnFiles"
    sequence_files = os.listdir(sequence_data_path)
    file_len = len(sequence_files)
    if testing:
        sequence_files = sequence_files[0:50]
        start = time.time()
    rows_to_write = []
    for file in sequence_files:
        if counter % 250 == 0:
            print(f"Writing {counter} of {file_len}")
            f = open(analysis_report_path, "a")
            for r in rows_to_write:
                f.write(r)
            f.close()
            rows_to_write = []
        name = file.split(".")[0]
        data_type = name.split("_")[1]
        dbn_file_path = f"{dbn_path}/{name}.dbn"
        dbn_file = open(dbn_file_path)
        data = dbn_file.readlines()
        true_structure = data[4].strip()
        seq = data[3].strip()
        if not sequence_is_only_nts(seq):
            weird_sequences.append(name)
            skipped += 1
            continue
        try:
            line_to_write = ""
            if model_name == "ContextFold":
                model.execute(model_path, seq)
            else:
                model.execute(model_path, f"{sequence_data_path}/{file}", remove_file_when_done=False)
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
            lengths.append(len(seq))
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

    if testing:
        end = time.time()
        elapsed = end - start
        avg = len(sequence_files) / elapsed
        projected_time = (file_len * avg) / 60 / 60

    # Get auxilary data
    aux_data = f"Data points evaluated: {counter}\n"
    aux_data += f"Longest sequence: {max(lengths)}\n"
    aux_data += f"Shortest sequence: {min(lengths)}\n"
    aux_data += f"Average sequence length: {sum(lengths) / len(lengths)}\n"
    aux_data += f"Skipped {skipped} files for throwing exceptions\n"

    if testing:
        aux_data += f"Projected time to complete all files: {round(projected_time, 2)} hours\n"

    if len(weird_sequences) != 0:
        aux_data += "Files with non-nucleotides in the sequence:\n"
        for ws in weird_sequences:
            aux_data += f"{ws}\n"

    aux_data += f"Report generated on: {datetime.datetime.now()}\n\n"
    aux_file = open(aux_data_path, "w")
    aux_file.write(aux_data)
    aux_file.close()

def sequence_is_only_nts(seq):
    nucleotides = {"A", "C", "U", "G", "a", "c", "u", "g"}
    seq_chars = set(seq)
    for sc in seq_chars:
        if sc not in nucleotides:
            return False
    return True



print("starting ...")
generate_c_bpRNA_evaluations(
    model=model,
    model_name=model_name,
    model_path=model_path,
    testing=True
)
print("done")
