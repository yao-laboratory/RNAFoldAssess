import os, datetime, time

import pandas as pd

from RNAFoldAssess.models import DataPoint, EternaDataPoint, DataPointFromCrystal
from RNAFoldAssess.models.scorers import *
from RNAFoldAssess.utils.secondary_structure_tools import SecondaryStructureTools

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

def generate_eterna_data_evaluations(model,
                                     model_name,
                                     model_path,
                                     data_points_path="/common/yesselmanlab/ewhiting/data/translated_eterna_data/eterna.json",
                                     data_type_name="EternaRDATData",
                                     to_seq_file=False,
                                     testing=False):
    datapoints = EternaDataPoint.factory(data_points_path)
    if testing:
        datapoints = datapoints[:10]
    shape_datapoints = []
    dms_datapoints = []

    fail_count = 0
    for dp in datapoints:
        if dp.mapping_method == "SHAPE":
            shape_datapoints.append(dp)
        elif dp.mapping_method == "DMS":
            dms_datapoints.append(dp)
        else:
            print(f"Error in {dp.name}")
            fail_count += 1

    print(f"There are {len(shape_datapoints)} SHAPE datapoints")
    print(f"There are {len(dms_datapoints)} DMS datapoints")
    print(f"There were {fail_count} errors detecting chemical mapping experiment type")

    headers = "algo_name, datapoint_name, sequence, prediction, accuracy, p_value, sequence_length"
    shape_report_path = f"/mnt/nrdstor/yesselmanlab/ewhiting/reports/eterna_data/{model_name}_SHAPE_pipeline_report.txt"
    dms_report_path = f"/mnt/nrdstor/yesselmanlab/ewhiting/reports/eterna_data/{model_name}_DMS_pipeline_report.txt"

    # Run SHAPE evals
    print("Starting SHAPE evaluations")
    shape_evals, problem_datapoints, s_skipped = eterna_data_evals(model, model_name, model_path, shape_datapoints, to_seq_file)
    if len(shape_evals) > 0:
        sf = open(shape_report_path, "w")
        sf.write(f"{headers}\n")
        for sev in shape_evals:
            line = f"{model_name}, {sev[0]}, {sev[1]}, {sev[2]}, {sev[3]}, {sev[4]}, {sev[5]}\n"
            sf.write(line)
        sf.close()
        write_eterna_data_analysis(model_name, shape_evals, problem_datapoints, s_skipped, "SHAPE")
    print("SHAPE evaluation complete")
    # Run DMS evals
    print("Starting DMS evaluations")
    dms_evals, problem_datapoints, d_skipped = eterna_data_evals(model, model_name, model_path, dms_datapoints, to_seq_file)
    if len(dms_evals) > 0:
        df = open(dms_report_path, "w")
        df.write(f"{headers}\n")
        for dev in dms_evals:
            line = f"{model_name}, {dev[0]}, {dev[1]}, {dev[2]}, {dev[3]}, {dev[4]}, {dev[5]}\n"
            df.write(line)
        df.close()
        write_eterna_data_analysis(model_name, dms_evals, problem_datapoints, d_skipped, "DMS")
    print("DMS evaluation complete")

def write_eterna_data_analysis(model_name, evals, problems, skipped, chemical_mapping_method, partition_number=None):
    count_problems = len(problems)
    accuracies = []
    lengths = []
    perfect_score_count = 0
    for ev in evals:
        acc = ev[1]
        if acc == 1.0:
            perfect_score_count += 1
        accuracies.append(acc)
        lengths.append(ev[3])
    s = pd.Series(accuracies)
    descriptive_stats = s.describe()
    report = f"{model_name} evaluation on Eterna {chemical_mapping_method}\n"
    report += f"Evaluated {len(evals)} datapoints\n"
    report += f"Skipped {skipped} datapoints due to exceptions\n"
    report += f"Using DSCI, {perfect_score_count} predictions achieved a perfect score\n"
    report += f"Descriptive statistics:\n"
    report += f"{descriptive_stats}\n"
    if len(problems) > 0:
        report += "\nSkipped datapoints:\n"
        for p in problems:
            report += f"{p}\n"
        report += "\n"
    report += f"Report generated on: {datetime.datetime.now()}\n\n"
    if partition_number:
        path = f"/mnt/nrdstor/yesselmanlab/ewhiting/reports/eterna_data/{model_name}_{chemical_mapping_method}_partition-{partition_number}_analysis_report.txt"
    else:
        path = f"/mnt/nrdstor/yesselmanlab/ewhiting/reports/eterna_data/{model_name}_{chemical_mapping_method}_analysis_report.txt"
    f = open(path, "w")
    f.write(report)
    f.close()

def eterna_data_evals(model, model_name, model_path, data_points, to_seq_file, delete_seq_file=True):
    retvals = []
    problem_datapoints = []
    skipped = 0
    counter = 0
    for dp in data_points:
        counter += 1
        if counter % 150 == 0:
            print(f"Working on {counter} of {len(data_points)}")
        if model_name not in ["ContextFold", "SeqFold", "NUPACK"]:
            if to_seq_file:
                input_file_path = dp.to_seq_file()
            else:
                input_file_path = dp.to_fasta_file()
        try:
            line_to_write = ""
            # Handle different model types
            if model_name in ["ContextFold", "SeqFold"]:
                model.execute(model_path, dp.sequence)
            elif model_name in ["RandomPredictor", "RNAStructure"] or "MXFold2" in model_name:
                model.execute(input_file_path, remove_file_when_done=True)
            elif model_name == "NUPACK":
                model.execute(dp.sequence)
            else:
                model.execute(model_path, input_file_path)
                if delete_seq_file:
                    os.remove(input_file_path)

            if model_name in ["IPKnot", "IPknot"]:
                predicted_structure = model.get_ss_prediction_ignore_pseudoknots()
            else:
                predicted_structure = model.get_ss_prediction()
            score = dp.assess_prediction(predicted_structure)
            retvals.append([dp.name, dp.sequence, predicted_structure, round(score["accuracy"], 4), round(score["p"], 4), len(dp.sequence)])
        except (DSCITypeError, DSCIValueError) as dsci_error:
            skipped += 1
            problem_datapoints.append(dp.name)
            print(f"Encountered DSCI error on {dp.name}: {str(dsci_error)}")
            continue
        except Exception as e:
            print(e)
            skipped += 1
            continue
    return retvals, problem_datapoints, skipped

def crystal_evals(model,
                  model_name,
                  model_path,
                  dbn_path="/common/yesselmanlab/ewhiting/data/crystal_all/release_2024/long_dbns",
                  data_type_name="crystal",
                  fasta_file_location="/common/yesselmanlab/ewhiting/data/crystal_all/release_2024/longFastaFiles",
                  to_seq_file=False,
                  leniences=[0, 1],
                  testing=False):
    headers = "algo_name, datapoint_name, lenience, sequence, prediction, sensitivity, ppv, f1"
    dps = DataPointFromCrystal.factory_from_dbn_files(dbn_path)
    if testing:
        dps = dps[:20]
    skipped = 0
    lengths = []
    problem_datapoints = []
    sensitivities = {}
    ppvs = {}
    f1s = {}
    lowest_sensitivity = {}
    lowest_ppv = {}
    lowest_f1 = {}
    for lenience in leniences:
        sensitivities[f"{lenience}"] = []
        ppvs[f"{lenience}"] = []
        f1s[f"{lenience}"] = []
        lowest_sensitivity[f"{lenience}"] = [1.0, ""]
        lowest_ppv[f"{lenience}"] = [1.0, ""]
        lowest_f1[f"{lenience}"] = [1.0, ""]

    analysis_report_path = f"/mnt/nrdstor/yesselmanlab/ewhiting/reports/crystal_release_2024/{model_name}_{data_type_name}_report.txt"
    pipeline_report_path = f"/mnt/nrdstor/yesselmanlab/ewhiting/reports/crystal_release_2024/{model_name}_{data_type_name}.txt"

    f = open(analysis_report_path, "w")
    f.write(f"{headers}\n")

    counter = 0
    skipped = 0
    dp_size = len(dps)

    print("About to run evaluation")
    for dp in dps:
        if len(dp.sequence) <= 1:
            skipped += 1
            print(f"Skipping {dp.name} because it is only one nucleotide long")
            continue
        if counter % 125 == 0:
            print(f"Completed {counter} of {dp_size} data points and {len(leniences)} leniences")
        lengths.append(len(dp.sequence))

        if model_name not in ["ContextFold", "SeqFold"]:
            if to_seq_file:
                input_file_path = dp.to_seq_file()
            else:
                input_file_path = f"{fasta_file_location}/{dp.name}.fasta"

        try:
            line_to_write = ""
            # Handle different model types
            if model_name in ["ContextFold", "SeqFold"]:
                model.execute(model_path, dp.sequence)
            elif model_name in ["RandomPredictor", "RNAStructure", "NUPACK"] or "MXFold2" in model_name:
                model.execute(input_file_path, remove_file_when_done=True)
            else:
                model.execute(model_path, input_file_path)

            if model_name == "IPKnot":
                prediction = model.get_ss_prediction_ignore_pseudoknots()
            else:
                prediction = model.get_ss_prediction()

        except:
            skipped += 1
            print(f"Skipping {dp.name} because of raised exception")
            continue

        for lenience in leniences:
            f.write(f"{model_name}, {dp.name}, {lenience}, {dp.sequence}, {prediction}, ")
            scorer = BasePairScorer(dp.true_structure, prediction, lenience)
            scorer.evaluate()
            s = scorer.sensitivity
            p = scorer.ppv
            f1 = scorer.f1
            sensitivities[f"{lenience}"].append(s)
            ppvs[f"{lenience}"].append(p)
            f1s[f"{lenience}"].append(f1)

            if s < lowest_sensitivity[f"{lenience}"][0]:
                lowest_sensitivity[f"{lenience}"][0] = s
                lowest_sensitivity[f"{lenience}"][1] = dp.name

            if p < lowest_ppv[f"{lenience}"][0]:
                lowest_ppv[f"{lenience}"][0] = p
                lowest_ppv[f"{lenience}"][1] = dp.name

            if f1 < lowest_f1[f"{lenience}"][0]:
                lowest_f1[f"{lenience}"][0] = f1
                lowest_f1[f"{lenience}"][1] = dp.name

            f.write(f"{s}, {p}, {f1}\n")
        counter += 1

    f.close()
    about_data = ""
    about_data += f"About {data_type_name} dataset\n"
    about_data += f"Datapoints evaluated: {len(lengths)}\n"
    about_data += f"Longest sequence: {max(lengths)}\n"
    about_data += f"Shortest sequence: {min(lengths)}\n"
    about_data += f"Most common lenth length: {max(set(lengths), key=lengths.count)}\n"
    about_data += f"Skipped {skipped} datapoints because of raised exceptions\n"
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

    about_data += f"Report generated on: {datetime.datetime.now()}\n\n"
    f2 = open(pipeline_report_path, "w")
    f2.write(about_data)
    f2.close()


def generate_rnandria_evaluations(model, model_name, model_path, source_data_path, source_type, to_seq_file=False, testing=False):
    headers = "algo_name, datapoint_name, sequence, prediction, accuracy, p_value, sequence_length"
    skipped = 0
    counter = 0
    length_skip_threshold = 5
    problem_datapoints = []
    report_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/rnandria"
    report_path = f"{model_name}_rnandria_{source_type}_predictions.txt"
    problem_path = f"{model_name}_rnandria_{source_type}_problems.txt"
    report_file = open(f"{report_dir}/{report_path}", "w")
    problem_file = open(f"{report_dir}/{problem_path}", "w")
    dps = DataPoint.factory(source_data_path)

    print("Loading datapoints")
    if testing:
        dps = dps[:20]
    dp_count = len(dps)
    print(f"Loaded {dp_count} data points")
    rows_to_write = []
    for dp in dps:
        if len(dp.sequence) <= 1:
            skipped += 1
            problem_file.write(f"{dp.name} Can't predict base pairing for one nucleotide\n")
            continue
        if len(dp.sequence) < length_skip_threshold:
            # Want to skip these because we think a secondary structure cannot
            # form if it's less than 5 nucleotides long. Don't want to add to
            # the skipped count, just continue.
            continue
        if counter % 200 == 0:
            print(f"Completed {counter} of {dp_count}")
            for r in rows_to_write:
                report_file.write(r)
            rows_to_write = []

        if model_name not in ["ContextFold", "SeqFold", "NUPACK"]:
            if to_seq_file:
                input_file_path = dp.to_seq_file()
            else:
                input_file_path = dp.to_fasta_file()
        else:
            # These two models can take string input
            input_file_path = dp.sequence
        try:
            # Handle different model types
            if model_name in ["ContextFold", "SeqFold"]:
                if model_name == "ContextFold" and len(dp.sequence) < 10:
                    skipped += 1
                    problem_file.write(f"Can't predict for {dp.name} of sequence \"{dp.sequence}\" - nt must be > 10\n")
                    continue
                if model_name == "SeqFold" and len(dp.sequence) < 2:
                    skipped += 1
                    problem_file.write(f"Can't predict for {dp.name} of sequence \"{dp.sequence}\" - nt must be > 2\n")
                    continue
                model.execute(model_path, dp.sequence)
            elif model_name in ["RandomPredictor", "RNAStructure", "NUPACK"] or "MXFold2" in model_name:
                model.execute(input_file_path, remove_file_when_done=True)
            else:
                model.execute(model_path, input_file_path)

            if model_name == "IPKnot":
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

            line_to_write = f"{model_name}, {dp.name}, {dp.sequence}, {prediction}, {accuracy}, {p}, {len(dp.sequence)}\n"
            rows_to_write.append(line_to_write)

            counter += 1

            if to_seq_file:
                os.remove(input_file_path)

        except (DSCITypeError, DSCIValueError) as dsci_error:
            skipped += 1
            problem_to_write = f"{dp.name}, {dsci_error}, {prediction}\n"
            problem_file.write(problem_to_write)
            continue

        except Exception as e:
            skipped += 1
            problem_to_write = f"{dp.name}, {e}\n"
            problem_file.write(problem_to_write)

    if len(rows_to_write) != 0:
        for r in rows_to_write:
            report_file.write(r)
            rows_to_write = []

    report_file.close()
    problem_file.close()



def generate_rasp_data(model,
                       model_name,
                       model_path,
                       data_path,
                       data_type_name,
                       file_prefix,
                       species,
                       to_seq_file=False,
                       testing=False,
                       chemical_mapping_method="DMS",
                       part_2=False):
    headers = "algo_name, datapoint_name, sequence, prediction, accuracy, p_value"
    skipped = 0
    lengths = []
    problem_datapoints = []
    generated_report_path = f"/mnt/nrdstor/yesselmanlab/ewhiting/reports/rasp_data/{species}/{model_name}/{model_name}_{file_prefix}_predictions.txt"
    problem_datapoint_path = f"/mnt/nrdstor/yesselmanlab/ewhiting/reports/rasp_data/{species}/{model_name}/{model_name}_{file_prefix}_problems.txt"
    print(f"Loading datapoints")
    dps = DataPoint.factory(data_path)
    # Remove data points that are only 1 nucleotide long
    # 1-nt sequence cannot form a secondary structure
    for dp in dps:
        if len(dp.sequence) == 1:
            dps.remove(dp)
    dp_count = len(dps)
    print(f"Loaded {dp_count} datapoints")
    if testing:
        dps = dps[200:400]

    if part_2:
        generated_report_path += ".2.txt"
        problem_datapoint_path += ".2.txt"
    report_file = open(generated_report_path, "w")
    report_file.write(headers + "\n")
    problem_file = open(problem_datapoint_path, "w")

    print("About to generate evaluations")
    if testing:
        start = time.time()

    counter = 0
    rows_to_write = []
    length_skip_threshold = 5
    for dp in dps:
        if len(dp.sequence) <= 1:
            skipped += 1
            problem_file.write(f"{dp.name} Can't predict base pairing for one nucleotide\n")
            continue
        if len(dp.sequence) < length_skip_threshold:
            # Want to skip these because we think a secondary structure cannot
            # form if it's less than 5 nucleotides long. Don't want to add to
            # the skipped count, just continue.
            continue
        if counter % 200 == 0:
            print(f"Completed {counter} of {dp_count}")
            for r in rows_to_write:
                report_file.write(r)
            rows_to_write = []

        if model_name not in ["ContextFold", "SeqFold", "NUPACK"]:
            if to_seq_file:
                input_file_path = dp.to_seq_file()
            else:
                input_file_path = dp.to_fasta_file()
        else:
            # These two models can take string input
            input_file_path = dp.sequence
        try:
            # Handle different model types
            if model_name in ["ContextFold", "SeqFold"]:
                if model_name == "ContextFold" and len(dp.sequence) < 10:
                    skipped += 1
                    problem_file.write(f"Can't predict for {dp.name} of sequence \"{dp.sequence}\" - nt must be > 10\n")
                    continue
                if model_name == "SeqFold" and len(dp.sequence) < 2:
                    skipped += 1
                    problem_file.write(f"Can't predict for {dp.name} of sequence \"{dp.sequence}\" - nt must be > 2\n")
                    continue
                model.execute(model_path, dp.sequence)
            elif model_name in ["RandomPredictor", "RNAStructure", "NUPACK"] or "MXFold2" in model_name:
                model.execute(input_file_path)
            else:
                model.execute(model_path, input_file_path)

            if model_name in ["IPknot", "IPKnot"]:
                prediction = model.get_ss_prediction_ignore_pseudoknots()
            else:
                prediction = model.get_ss_prediction()

            if chemical_mapping_method == "DMS":
                score = DSCI.score(
                    dp.sequence,
                    prediction,
                    dp.reactivities,
                    DMS=True
                )
            else:
                score = DSCI.score(
                    dp.sequence,
                    prediction,
                    dp.reactivities,
                    SHAPE=True
                )

            accuracy = round(score["accuracy"], 4)
            p = round(score["p"], 4)

            line_to_write = f"{model_name}, {dp.name}, {dp.sequence}, {prediction}, {accuracy}, {p}\n"
            rows_to_write.append(line_to_write)

            lengths.append(len(dp.sequence))
            counter += 1

            if to_seq_file:
                os.remove(input_file_path)

        except (DSCITypeError, DSCIValueError) as dsci_error:
            skipped += 1
            problem_to_write = f"{dp.name}, {dsci_error}, {prediction}\n"
            problem_file.write(problem_to_write)
            continue

        except Exception as e:
            skipped += 1
            problem_to_write = f"{dp.name}, {e}\n"
            problem_file.write(problem_to_write)

    if len(rows_to_write) != 0:
        for r in rows_to_write:
            report_file.write(r)
            rows_to_write = []

    report_file.close()
    problem_file.close()

    if testing:
        end = time.time()
        elapsed = end - start
        avg = len(dps) / elapsed
        projected_time = (dp_count * avg) / 60 / 60

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

    aux_data_path = f"/mnt/nrdstor/yesselmanlab/ewhiting/reports/rasp_data/{species}/{model_name}/{model_name}_{file_prefix}_aux_data.txt"
    aux_data += f"Report generated on: {datetime.datetime.now()}\n\n"
    aux_file = open(aux_data_path, "w")
    aux_file.write(aux_data)
    aux_file.close()


def parallel_bprna_predictions(model,
                               model_name,
                               model_path,
                               partition_number,
                               data_type_name="bpRNA-1m-90",
                               to_seq_file=False,
                               testing=False):
    sequence_data_path = "/work/yesselmanlab/ewhiting/data/bprna/fastaFiles"
    dbn_data_path = f"/work/yesselmanlab/ewhiting/data/bprna/dbnFiles_sep/part_{partition_number}/"
    headers = "algo_name, datapoint_name, lenience, sequence, true_structure, prediction, sensitivity, ppv, F1\n"
    skipped = 0
    analysis_report_path = f"/mnt/nrdstor/yesselmanlab/ewhiting/reports/bprna/{model_name}_{data_type_name}_{partition_number}_report.txt"

    # make the file
    report = open(analysis_report_path, "w")
    report.write(headers)
    counter = 0

    dbn_files = os.listdir(dbn_data_path)

    if testing:
        dbn_files = dbn_files[:10]

    for file in dbn_files:
        if counter % 250 == 0:
            print(f"Working {counter}")

        dbn_file = open(f"{dbn_data_path}/{file}")
        dbn_data = [d.strip() for d in dbn_file.readlines()]
        dbn_file.close()
        seq = dbn_data[3]
        dbn = dbn_data[4]
        if not sequence_is_only_nts(seq):
            print(f"{seq} sequence contains more than just ACUG nucleotides")
            skipped += 1
            continue

        # Clean DBN
        dbn = dbn.replace("<", ".").replace(">", ".").replace("{", ".").replace("}", ".")

        created_fasta_file = False
        name = file.split(".")[0]
        seq_file_path = f"{sequence_data_path}/{name}.fasta"
        if not os.path.exists(seq_file_path):
            print(f"No fasta file at {seq_file_path}. Creating.")
            fasta_data = f">{name}\n{seq}"
            ff = open(f"{name}.fasta", "w")
            ff.write(fasta_data)
            ff.close()
            created_fasta_file = True
            seq_file_path = f"{name}.fasta"

        try:
            line_to_write = ""
            if model_name in ["ContextFold", "SeqFold"]:
                # These models don't require an input file
                model.execute(model_path, seq)
            elif model_name == "NUPACK":
                model.execute(seq)
            elif model_name in ["RandomPredictor", "RNAStructure"] or "MXFold2" in model_name:
                model.execute(seq_file_path)
            elif model_name.lower() == "pknots":
                model.execute(seq_file_path, "bprna")
            else:
                model.execute(model_path, seq_file_path, remove_file_when_done=False)
            if model_name in ["IPknot", "IPKnot"]:
                prediction = model.get_ss_prediction_ignore_pseudoknots()
            else:
                prediction = model.get_ss_prediction()
            for lenience in [0, 1]:
                line_to_write = f"{model_name}, {name}, {lenience}, "
                scorer = BasePairScorer(dbn, prediction, lenience)
                scorer.evaluate()
                s = scorer.sensitivity
                p = scorer.ppv
                f1 = scorer.f1
                line_to_write += f"{seq}, {dbn}, {prediction}, {s}, {p}, {f1}\n"
                report.write(line_to_write)
            if created_fasta_file:
                print(f"Removing {seq_file_path}")
                os.remove(seq_file_path)
            counter += 1
        except Exception as e:
            print(f"Exception in {file}: {e}")
            skipped += 1
            # continue

    print(f"Skipped {skipped}")
    report.close()


def generate_ribonanza_evaluations(model,
                                   model_name,
                                   model_path,
                                   to_seq_file=False,
                                   testing=False,
                                   part2=False):
    ribo_data_csv = "/mnt/nrdstor/yesselmanlab/ewhiting/rna_data/ribonanza/rmdb_data.v1.3.0.csv"
    f = open(ribo_data_csv)
    data = f.readlines()
    f.close()
    # Get rid of headers
    data.pop(0)
    data = [d.split(",") for d in data]
    r1_index = 7
    # Experiment types:
    # {'BzCN_cotx', 'deg_Mg_50C', 'BzCN', 'DMS_M2_seq', 'deg_pH10', 'deg_Mg_pH10', 'DMS_cotx', 'deg_50C', 'NMIA', 'DMS', 'CMCT', '1M7'
    experiment_map = {
        "BzCN_cotx": "DMS4",
        "DMS_M2_seq": "DMS4",
        "DMS_cotx": "DMS4",
        "DMS": "DMS4",
        "1M7": "SHAPE",
        "NMIA": "SHAPE",
        "BzCN": "SHAPE",
        "deg_Mg_50C": "SHAPE",
        "deg_50C": "SHAPE",
        "deg_pH10": "SHAPE",
        "deg_Mg_pH10": "SHAPE",
        "CMCT": "CMCT"
    }
    report_path = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/ribonanza/with_energies"

    # Create report file map
    report_files = {}
    for k in experiment_map:
        if part2:
            f = open(f"{report_path}/{model_name}_{k}_predictions2.txt", "w")
        else:
            f = open(f"{report_path}/{model_name}_{k}_predictions.txt", "w")
        report_files[k] = f

    # Create problem file map
    problem_files = {}
    for k in experiment_map:
        if part2:
            f = open(f"{report_path}/{model_name}_{k}_problems2.txt", "w")
        else:
            f = open(f"{report_path}/{model_name}_{k}_problems.txt", "w")
        problem_files[k] = f

    if testing:
        data = data[:10]

    # Run Evaluations
    print("Starting evaluations")
    counter = 0
    for d in data:
        name = d[0]
        seq = d[1]
        experiment_type = d[2]
        chemical_mapping_method = experiment_map[experiment_type]
        report_file = report_files[experiment_type]
        problem_file = problem_files[experiment_type]
        reactivities = d[r1_index:len(seq) + r1_index]
        testable_seq = ""
        testable_reactivities = []
        for i, reactivity in enumerate(reactivities):
            if reactivity != "":
                testable_seq += seq[i]
                testable_reactivities.append(float(reactivity))

        sequence = testable_seq
        reactivities = testable_reactivities
        if len(sequence) < 2:
            # Can't predict secondary structure on one nucleotide
            continue

        dp = DataPoint({
            "name": name,
            "sequence": sequence,
            "data": reactivities,
            "reads": 0
        })
        if counter % 200 == 0:
            print(f"Completed {counter} of {len(data)}")

        if model_name not in ["ContextFold", "SeqFold", "NUPACK"]:
            if to_seq_file:
                input_file_path = dp.to_seq_file()
            else:
                input_file_path = dp.to_fasta_file()
        else:
            # These three models can take string input
            input_file_path = dp.sequence
        try:
            # Handle different model types
            if model_name in ["ContextFold", "SeqFold"]:
                if model_name == "ContextFold" and len(dp.sequence) < 10:
                    problem_file.write(f"Can't predict for {dp.name} of sequence \"{dp.sequence}\" - nt must be > 10\n")
                    continue
                if model_name == "SeqFold" and len(dp.sequence) < 2:
                    problem_file.write(f"Can't predict for {dp.name} of sequence \"{dp.sequence}\" - nt must be > 2\n")
                    continue
                model.execute(model_path, dp.sequence)
            elif model_name in ["RandomPredictor", "RNAStructure", "NUPACK"] or "MXFold2" in model_name:
                model.execute(input_file_path, remove_file_when_done=True)
            else:
                model.execute(model_path, input_file_path)

            if model_name == "IPKnot":
                prediction = model.get_ss_prediction_ignore_pseudoknots()
            else:
                prediction = model.get_ss_prediction()

            testable_prediction = prediction[:len(sequence)]
            if chemical_mapping_method in ["DMS4", "SHAPE"]:
                score = DSCI.score(
                    sequence,
                    testable_prediction,
                    reactivities,
                    SHAPE=True
                )
            else:
                score = DSCI.score(
                    sequence,
                    testable_prediction,
                    reactivities,
                    CMCT=True
                )

            accuracy = round(score["accuracy"], 4)
            p = round(score["p"], 4)
            # Get free energy
            if model_name == "RNAStructure":
                fe = model.mfe
            elif model_name == "NUPACK":
                fe = model.get_mfe()
            else:
                fe = SecondaryStructureTools.get_free_energy(testable_seq, testable_prediction)
            line_to_write = f"{model_name}, {dp.name}, {testable_seq}, {testable_prediction}, {accuracy}, {p}, {fe}\n"
            report_file.write(line_to_write)
            counter += 1

        except (DSCITypeError, DSCIValueError) as dsci_error:
            problem_to_write = f"{dp.name}, {dsci_error}, {prediction}\n"
            problem_file.write(problem_to_write)
            continue

        except Exception as e:
            problem_to_write = f"{dp.name}, {e}\n"
            problem_file.write(problem_to_write)

    for k in experiment_map:
        report_files[k].close()
        problem_files[k].close()


def generate_dms_evaluations(model,
                               model_name,
                               model_path,
                               sequence_data_path="/common/yesselmanlab/ewhiting/data/bprna/fasta_files",
                               dp_file_path="/common/yesselmanlab/ewhiting/ss_deeplearning_data/data",
                               reports_dir="ydata",
                               data_type_name="YesselmanDMS",
                               to_seq_file=False,
                               testing=False):
    approved_chorots = [
        "C014G",
        "C014H",
        "C014I",
        "C014J",
        "C014U",
        "C014V"
    ]
    headers = "algo_name, datapoint_name, sequence, prediction, accuracy, p_value"
    skipped = 0
    lengths = []
    problem_datapoints = []
    data_point_files = os.listdir(dp_file_path)
    analysis_report_path = f"/mnt/nrdstor/yesselmanlab/ewhiting/reports/{reports_dir}/{model_name}_{data_type_name}_report.txt"
    aux_data_path = f"/mnt/nrdstor/yesselmanlab/ewhiting/reports/{reports_dir}/{model_name}_{data_type_name}_aux_data.txt"

    print(f"Loading data points from {len(data_point_files)} files ...")
    data_points = []
    for dpf in data_point_files:
        cohort = dpf.split(".")[0]
        if cohort not in approved_chorots:
            continue
        print(f"Loading data points from {cohort} cohort")
        dps = DataPoint.factory(f"{dp_file_path}/{dpf}", cohort)
        for dp in dps:
            data_points.append(dp)

    if testing:
        data_points = data_points[:20]
    file_len = len(data_points)

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
        made_a_file = False
        if counter % 250 == 0:
            print(f"Completed {counter} of {dp_size}")
            f = open(analysis_report_path, "a")
            for r in rows_to_write:
                f.write(r)
            f.close()
            rows_to_write = []

        if model_name not in ["ContextFold", "SeqFold", "NUPACK"]:
            if to_seq_file:
                input_file_path = dp.to_seq_file()
                made_a_file = True
            else:
                input_file_path = dp.to_fasta_file()
                made_a_file = True
        else:
            input_file_path = dp.sequence
        try:
            line_to_write = ""
            # Handle different model types
            if model_name in ["ContextFold", "SeqFold"]:
                model.execute(model_path, dp.sequence)
            elif model_name in ["RandomPredictor", "RNAStructure", "NUPACK"] or "MXFold2" in model_name:
                model.execute(input_file_path, remove_file_when_done=True)
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

            line_to_write = f"{model_name}, {dp.name}, {dp.sequence}, {prediction}, {round(accuracy, 4)}, {round(p, 4)}\n"
            rows_to_write.append(line_to_write)

            lengths.append(len(dp.sequence))
            counter += 1

            # if made_a_file:
            #     os.remove(input_file_path)

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

def analyze_dms_evaluations(loc, model_name, data_type="YesselmanLabDMS"):
    f = open(loc)
    data = f.readlines()
    f.close()
    data.pop(0) # Get rid of headers

    accuracies = []
    p_values = []
    lowest_acc = [None, 1.0]
    highest_p = [None, 0.0]
    perfect_score_count = 0

    total_rows = len(data)

    counter = 0
    for d in data:
        if counter % 250 == 0:
            print(f"Processing {counter} of {total_rows}")
        d = d.split(",")
        name = d[1].strip()
        acc = float(d[2].strip())
        p = float(d[3].strip())
        accuracies.append(acc)
        p_values.append(p)
        if acc == 1.0:
            perfect_score_count += 1
        if acc < lowest_acc[1]:
            lowest_acc = [name, acc]
        if p > highest_p[1]:
            highest_p = [name, p]
        counter += 1

    write_dms_pipeline_report(
        model_name,
        data_type,
        accuracies,
        p_values,
        perfect_score_count,
        lowest_acc,
        highest_p
    )

def write_dms_pipeline_report(model_name,
                              data_type,
                              accuracies,
                              p_values,
                              perfect_score_count,
                              lowest_acc,
                              highest_p):
    avg_acc = sum(accuracies) / len(accuracies)
    mode_acc = max(set(accuracies), key=accuracies.count)
    avg_p   = sum(p_values) / len(p_values)

    about_data = ""
    about_data += f"{model_name} Performance:\n"
    about_data += f"Data points evaluated: {len(accuracies)}\n"
    about_data += f"Average DSCI accuracy score: {round(avg_acc, 4)}\n"
    about_data += f"Average DSCI p-vale score: {avg_p}\n"
    about_data += f"Mode accuracy: {mode_acc}\n"
    about_data += f"Number of DSCI 1.0 scores: {perfect_score_count}\n"
    about_data += f"Lowest DSCI accruracy score: {lowest_acc[1]} on {lowest_acc[0]}\n"
    about_data += f"Highest DSCI p-value score: {highest_p[1]} on {highest_p[0]}\n"

    about_data += f"\n"
    about_data += f"Report generated on: {datetime.datetime.now()}\n\n"

    pipeline_report_path = f"/common/yesselmanlab/ewhiting/reports/ydata/{model_name}_{data_type}_analysis.txt"
    f = open(pipeline_report_path, "w")
    f.write(about_data)
    f.close()


def write_pipeline_report(predictor_name,
                          data_type,
                          lengths,
                          accuracies,
                          p_values,
                          perfects,
                          lowest_acc,
                          highest_p,
                          skipped_count):
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

def analyze_bprna_evaluations(eval_location, model_name):
    f = open(eval_location)
    rows = f.readlines()
    f.close()

    sensitivities = {}
    ppvs = {}
    f1s = {}
    lowest_sensitivity = {}
    lowest_ppv = {}
    lowest_f1 = {}
    leniences = [0, 1]
    for lenience in leniences:
        sensitivities[f"{lenience}"] = []
        ppvs[f"{lenience}"] = []
        f1s[f"{lenience}"] = []
        lowest_sensitivity[f"{lenience}"] = [1.0, ""]
        lowest_ppv[f"{lenience}"] = [1.0, ""]
        lowest_f1[f"{lenience}"] = [1.0, ""]

    count_of_rows = len(rows)
    counter = 0

    print(f"Starting analysis on {count_of_rows} datapoints ...")

    for r in rows:
        r = r.split(",")
        name = r[1].strip()
        recorded_lenience = int(r[2].strip())

        counter += 1
        if counter % 250 == 0:
            print(f"Working on {counter} of {count_of_rows}")
        for lenience in leniences:
            if recorded_lenience == lenience:
                s = float(r[3].strip())
                p = float(r[4].strip())
                f1 = float(r[5].strip())
                sensitivities[f"{lenience}"].append(s)
                ppvs[f"{lenience}"].append(p)
                f1s[f"{lenience}"].append(f1)

                if s < lowest_sensitivity[f"{lenience}"][0]:
                    lowest_sensitivity[f"{lenience}"][0] = s
                    lowest_sensitivity[f"{lenience}"][1] = name

                if p < lowest_ppv[f"{lenience}"][0]:
                    lowest_ppv[f"{lenience}"][0] = p
                    lowest_ppv[f"{lenience}"][1] = name

                if f1 < lowest_f1[f"{lenience}"][0]:
                    lowest_f1[f"{lenience}"][0] = f1
                    lowest_f1[f"{lenience}"][1] = name

    pipeline_report_path = f"/common/yesselmanlab/ewhiting/reports/bprna/{model_name}_bpRNA_analysis.txt"
    write_bp_pipeline_report(
        pipeline_report_path,
        count_of_rows,
        leniences,
        sensitivities,
        lowest_sensitivity,
        ppvs,
        lowest_ppv,
        f1s,
        lowest_f1
    )



def generate_bpRNA_evaluations(model,
                               model_name,
                               model_path,
                               sequence_data_path="/common/yesselmanlab/ewhiting/data/bprna/fasta_files",
                               leniences=[0, 1],
                               testing=False):
    data_type_name = "bpRNA-1m-90"
    headers = "algo_name, datapoint_name, lenience, sequence,true_structure, prediction, sensitivity, ppv, F1, data_point_type"
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
        if not os.path.exists(dbn_file_path):
            print(f"No DBN file for {name}")
            continue
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
            elif model_name == "NUPACK":
                model.execute(seq)
            elif model_name in ["RandomPredictor", "RNAStructure"] or "MXFold2" in model_name:
                model.execute(f"{sequence_data_path}/{file}")
            else:
                model.execute(model_path, f"{sequence_data_path}/{file}", remove_file_when_done=False)
            if model_name in ["IPknot", "IPKnot"]:
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
                line_to_write += f"{seq},{true_structure}, {prediction}, {s}, {p}, {f1}\n"
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
