import os, datetime, time

import pandas as pd

from RNAFoldAssess.models import DataPoint, EternaDataPoint, DataPointFromCrystal
from RNAFoldAssess.models.scorers import *
from RNAFoldAssess.utils.secondary_structure_tools import SecondaryStructureTools
from RNAFoldAssess.utils.pipelines import eterna_data_evals, write_eterna_data_analysis


def generate_dms_evaluations_by_cohort_partition(model,
                                                model_name,
                                                model_path,
                                                cohort,
                                                partition_size=0,
                                                partition_number=0,
                                                sequence_data_path="/common/yesselmanlab/ewhiting/data/bprna/fasta_files",
                                                dp_file_path="/common/yesselmanlab/ewhiting/ss_deeplearning_data/data",
                                                reports_dir="ydata",
                                                data_type_name="YesselmanDMS",
                                                to_seq_file=False,
                                                testing=False,):
    approved_chorots = [
        "C014G",
        "C014H",
        "C014I",
        "C014J",
        "C014U",
        "C014V"
    ]

    if cohort not in approved_chorots:
        raise Exception("Unacceptable cohort")

    data_points = DataPoint.factory(f"{dp_file_path}/{cohort}.json", cohort)

    skipped = 0
    lengths = []
    problem_datapoints = []
    analysis_report_path = f"/common/yesselmanlab/ewhiting/reports/{reports_dir}/{model_name}_{cohort}_{data_type_name}_partition_{partition_number}_report.txt"
    aux_data_path = f"/common/yesselmanlab/ewhiting/reports/{reports_dir}/{model_name}_{cohort}_{data_type_name}_partition_{partition_number}_aux_data.txt"

    data_points = divide_list(datapoints, partition_size, partition_number)
    if testing:
        data_points = data_points[:20]
    file_len = len(data_points)

    dp_size = len(data_points)
    print(f"Total of {dp_size} data points")
    print("Data points loaded!")

    f = open(analysis_report_path, "w")
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

        if model_name not in ["ContextFold", "SeqFold"]:
            if to_seq_file:
                input_file_path = dp.to_seq_file()
                made_a_file = True
            else:
                input_file_path = dp.to_fasta_file()
                made_a_file = True
        try:
            line_to_write = ""
            # Handle different model types
            if model_name in ["ContextFold", "SeqFold"]:
                model.execute(model_path, dp.sequence)
            elif model_name in ["RandomPredictor", "MXFold2"]:
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

            line_to_write = f"{model_name}, {dp.name}, {dp.sequence}, {prediction}, {round(accuracy, 4)}, {round(p, 4)}\n"
            rows_to_write.append(line_to_write)

            lengths.append(len(dp.sequence))
            counter += 1

            if made_a_file:
                os.remove(input_file_path)

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
        avg = file_len / elapsed
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


def generate_dms_evaluations_by_cohort(model,
                               model_name,
                               model_path,
                               cohort,
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

    if cohort not in approved_chorots:
        raise Exception("Unacceptable cohort")

    data_points = DataPoint.factory(f"{dp_file_path}/{cohort}.json", cohort)

    skipped = 0
    lengths = []
    problem_datapoints = []
    analysis_report_path = f"/mnt/nrdstor/yesselmanlab/ewhiting/reports/{reports_dir}/{model_name}_{cohort}_{data_type_name}_report.txt"
    aux_data_path = f"/mnt/nrdstor/yesselmanlab/ewhiting/reports/{reports_dir}/{model_name}_{cohort}_{data_type_name}_aux_data.txt"

    if testing:
        data_points = data_points[:20]
    file_len = len(data_points)

    dp_size = len(data_points)
    print(f"Total of {dp_size} data points")
    print("Data points loaded!")

    f = open(analysis_report_path, "w")
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

        if model_name not in ["ContextFold", "SeqFold"]:
            if to_seq_file:
                input_file_path = dp.to_seq_file()
                made_a_file = True
            else:
                input_file_path = dp.to_fasta_file()
                made_a_file = True
        try:
            line_to_write = ""
            # Handle different model types
            if model_name in ["ContextFold", "SeqFold"]:
                model.execute(model_path, dp.sequence)
            elif model_name in ["RandomPredictor"] or "MXFold2" in model_name:
                model.execute(input_file_path)
                os.system(f"rm {input_file_path}")
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

            if made_a_file:
                os.remove(input_file_path)

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
        avg = file_len / elapsed
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


def divide_list_into_four(data, partition_wanted):
    one = data[:len(data)//3]
    two = data[len(data)//3:(len(data)//3)*2]
    three = data[(len(data)//3)*2:(len(data)//3)*3]
    four = data[(len(data)//3)*3:]
    return [one, two, three, four][partition_wanted]


def divide_list(data, partition_size, partition_wanted):
    retval = []
    if partition_size == 0:
        return data

    offset = partition_size - 1
    for i in range(partition_size):
        start = (len(data) // offset) * i
        end = (len(data) // offset) * (i + 1)
        retval.append(data[start:end])
    retval = [r for r in retval if r]
    try:
        wanted = retval[partition_wanted]
    except IndexError as e:
        raise Exception(f"Index error on requested partition {partition_wanted}. Exception message: {e}")
    return retval[partition_wanted]


def generate_eterna_data_evaluations_by_partition(model,
                                     model_name,
                                     model_path,
                                     data_points_path="/common/yesselmanlab/ewhiting/data/translated_eterna_data/eterna.json",
                                     data_type_name="EternaRDATData",
                                     to_seq_file=False,
                                     testing=False,
                                     partition_size=0,
                                     partition_number=0):
    datapoints = EternaDataPoint.factory(data_points_path)
    datapoints = divide_list(datapoints, partition_size, partition_number)

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
    shape_report_path = f"/mnt/nrdstor/yesselmanlab/ewhiting/reports/eterna_data/{model_name}_partition-{partition_number}_SHAPE_pipeline_report.txt"
    dms_report_path = f"/mnt/nrdstor/yesselmanlab/ewhiting/reports/eterna_data/{model_name}_partition-{partition_number}_DMS_pipeline_report.txt"

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
        write_eterna_data_analysis(model_name, shape_evals, problem_datapoints, s_skipped, "SHAPE", partition_number)
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
        write_eterna_data_analysis(model_name, dms_evals, problem_datapoints, d_skipped, "DMS", partition_number)
    print("DMS evaluation compelte")
