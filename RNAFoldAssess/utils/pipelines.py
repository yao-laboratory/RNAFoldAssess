import os, datetime, time

from RNAFoldAssess.models import DataPoint
from RNAFoldAssess.models.scorers import *

headers = "algo_name, datapoint_name, accuracy, p_value, ground_truth_data_type"


def get_data_point_list_from_directory(dp_path):
    data_point_files = os.listdir(dp_path)
    print(f"Loading data points from {len(data_point_files)} files ...")

    data_points = []
    for dpf in data_point_files:
        cohort = dpf.split(".")[0]
        print(f"Loading data points from {cohort} cohort")
        dps = DataPoint.factory(f"{dp_path}/{dpf}", cohort)
        for dp in dps:
            data_points.append(dp)
    return data_points


def get_data_point_list_from_file(path, cohort=""):
    return DataPoint.factory(path, cohort)


def analysis_report_location(predictor_name, data_type):
    return f"/common/yesselmanlab/ewhiting/reports/{predictor_name}_{data_type}_pipeline_report.txt"

def pipeline_report_location(predictor_name, data_type):
    return f"/common/yesselmanlab/ewhiting/reports/{predictor_name}_{data_type}_pipeline.txt"

def generate_dms_evaluations(model,
                               model_name,
                               model_path,
                               sequence_data_path="/common/yesselmanlab/ewhiting/data/bprna/fasta_files",
                               dp_file_path="/common/yesselmanlab/ewhiting/ss_deeplearning_data/data",
                               data_type_name="YesselmanDMS",
                               to_seq_file=False,
                               testing=False):
    headers = "algo_name, datapoint_name, accuracy, p_value"
    skipped = 0
    lengths = []
    problem_datapoints = []
    data_point_files = os.listdir(dp_file_path)
    analysis_report_path = f"/common/yesselmanlab/ewhiting/reports/ydata/{model_name}_{data_type_name}_report.txt"
    aux_data_path = f"/common/yesselmanlab/ewhiting/reports/ydata/{model_name}_{data_type_name}_aux_data.txt"

    print(f"Loading data points from {len(data_point_files)} files ...")
    data_points = []
    for dpf in data_point_files:
        cohort = dpf.split(".")[0]
        print(f"Loading data points from {cohort} cohort")
        dps = DataPoint.factory(f"{dp_file_path}/{dpf}", cohort)
        for dp in dps:
            data_points.append(dp)

    file_len = len(data_points)

    if testing:
        data_points = data_points[17360:17410] # There's an error-prone data point in here

    dp_size = len(data_points)
    print(f"Total of {dp_size} data points")
    print("Data points loaded!")

    f = open(analysis_report_path, "w")
    f.write(f"{headers}\n")
    f.close()

    print("About to generate evaluations")
    if testing:
        start = time.time()

    counter = 0
    rows_to_write = []
    for dp in data_points:
        if counter % 250 == 0:
            print(f"Completed {counter} of {dp_size}")
            f = open(analysis_report_path, "a")
            for r in rows_to_write:
                f.write(r)
            f.close()
            rows_to_write = []

        if model_name not in ["ContextFold", "SeqFold"]:
            if to_seq_file:
                input_file_path = dp.to_seq_file()
            else:
                input_file_path = dp.to_fasta_file()
        try:
            line_to_write = ""
            # Handle different model types
            if model_name in ["ContextFold", "SeqFold"]:
                model.execute(model_path, dp.sequence)
            elif model_name == "RandomPredictor":
                model.execute(input_file_path)
            else:
                model.execute(model_path, input_file_path)

            if model_name == "IPknot":
                prediction = model.get_ss_prediction_ignore_pseudoknots()
            else:
                prediction = model.get_ss_prediction()

            score = DSCI.score(
                dp.sequence,
                prediction,
                dp.reactivities,
                DMS=True
            )

            accuracy = round(score["accuracy"], 4)
            p = round(score["p"], 4)

            headers = "algo_name, datapoint_name, accuracy, p_value"
            line_to_write = f"{model_name}, {dp.name}, {round(accuracy, 4)}, {round(p, 4)}\n"
            rows_to_write.append(line_to_write)

            lengths.append(len(dp.sequence))
            counter += 1

        except (DSCITypeError, DSCIValueError) as dsci_error:
            skipped += 1
            problem_datapoints.append(dp.name)
            print(f"Encountered DSCI error on {dp.name}: {str(dsci_error)}")
            continue

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
        avg = len(data_point_files) / elapsed
        projected_time = (file_len * avg) / 60 / 60

    # Get auxilary data
    if len(lengths) == 0:
        lengths = [1,2,3,4] # Some bs data to stop exceptions
    aux_data = f"Data points evaluated: {counter}\n"
    aux_data += f"Longest sequence: {max(lengths)}\n"
    aux_data += f"Shortest sequence: {min(lengths)}\n"
    aux_data += f"Average sequence length: {sum(lengths) / len(lengths)}\n"
    aux_data += f"Skipped {skipped} files for throwing exceptions\n"

    if testing:
        aux_data += f"Projected time to complete all files: {round(projected_time, 2)} hours\n"

    if len(problem_datapoints) != 0:
        aux_data += f"Skippped {len(problem_datapoints)} datapoints for throwing DSCI exceptions:\n"
        for pd in problem_datapoints:
            aux_data += f"{pd}\n"

    aux_data += f"Report generated on: {datetime.datetime.now()}\n\n"
    aux_file = open(aux_data_path, "w")
    aux_file.write(aux_data)
    aux_file.close()



def write_pipeline_report(predictor_name, data_type, lengths, accuracies, p_values, perfects, lowest_acc, highest_p, skipped_count):
    avg_seq_len = sum(lengths) / len(lengths)
    max_len = max(lengths)
    min_len = min(lengths)
    mode_len = max(set(lengths), key=lengths.count)

    avg_acc = sum(accuracies) / len(accuracies)
    mode_acc = max(set(accuracies), key=accuracies.count)
    avg_p   = sum(p_values) / len(p_values)

    about_data = ""
    about_data += f"About {data_type} dataset\n"
    about_data += f"Average sequence length: {avg_seq_len}\n"
    about_data += f"Longest sequence: {max_len}\n"
    about_data += f"Shortest sequence: {min_len}\n"
    about_data += f"Most common sequence length: {mode_len}\n"

    about_data += f"\nData points evaluated: {len(accuracies)}\n"
    about_data += f"Skipped {skipped_count} molecules due to exceptions\n"

    about_data += f"\n{predictor_name} Performance:\n"
    about_data += f"Average DSCI accuracy score: {round(avg_acc, 4)}\n"
    about_data += f"Average DSCI p-vale score: {avg_p}\n"
    about_data += f"Mode accuracy: {mode_acc}\n"
    about_data += f"Number of DSCI 1.0 scores: {perfects}\n"
    about_data += f"Lowest DSCI accruracy score: {lowest_acc[1]} on {lowest_acc[0]}\n"
    about_data += f"Highest DSCI p-value score: {highest_p[1]} on {highest_p[0]}\n"

    about_data += f"\n"
    about_data += f"Report generated on: {datetime.datetime.now()}\n\n"

    f = open(pipeline_report_location(predictor_name, data_type), "w")
    f.write(about_data)
    f.close()

def write_bp_pipeline_report(pipeline_report_path,
                             count_of_rows,
                             leniences,
                             sensitivities,
                             lowest_sensitivity,
                             ppvs,
                             lowest_ppv,
                             f1s,
                             lowest_f1):
    about_data = ""
    about_data += f"About bpRNA dataset\n"
    about_data += f"Datapoints evaluated: {count_of_rows / len(leniences)}\n"
    about_data += f"\n"
    about_data += f"About Evaluation\n"
    about_data += f"------------------\n"
    for lenience in leniences:
        about_data += f"For {lenience} basepair lenience:\n"
        sens = sensitivities[f"{lenience}"]
        ls = lowest_sensitivity[f"{lenience}"]
        ps = ppvs[f"{lenience}"]
        lp = lowest_ppv[f"{lenience}"]
        fs = f1s[f"{lenience}"]
        lf = lowest_f1[f"{lenience}"]
        about_data += f"    Average sensitivity: {round(sum(sens) / len(sens), 4)}\n"
        about_data += f"    Highest sensitivity: {max(sens)}\n"
        about_data += f"    Lowest sensitivity: {round(ls[0], 4)} on {ls[1]}\n"
        about_data += f"    Average PPV: {round(sum(ps) / len(ps), 4)}\n"
        about_data += f"    Highest PPV: {max(ps)}\n"
        about_data += f"    Lowest PPV: {round(lp[0], 4)} on {lp[1]}\n"
        about_data += f"    Average F1: {round(sum(fs) / len(fs), 4)}\n"
        about_data += f"    Highest F1: {max(fs)}\n"
        about_data += f"    Lowest F1: {round(lf[0], 4)} on {lf[1]}\n"
        about_data += "\n"

    report = open(pipeline_report_path, "w")
    report.write(about_data)
    report.close()


def generate_bpRNA_evaluations(model,
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
        dbn_file.close()
        true_structure = data[4].strip()
        seq = data[3].strip()
        if not sequence_is_only_nts(seq):
            weird_sequences.append(name)
            continue
        try:
            line_to_write = ""
            if model_name in ["ContextFold", "SeqFold"]:
                # These models don't require an input file
                model.execute(model_path, seq)
            elif model_name == "RandomPredictor":
                model.execute(f"{sequence_data_path}/{file}")
            else:
                model.execute(model_path, f"{sequence_data_path}/{file}", remove_file_when_done=False)
            if model_name == "IPknot":
                prediction = model.get_ss_prediction_ignore_pseudoknots()
            else:
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
        aux_data += f"Skippped {len(weird_sequences)} files with non-nucleotides in the sequence\n"

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
