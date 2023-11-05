import os, datetime

from RNAFoldAssess.models import DataPoint

headers = "algo_name, datapoint_name, accuracy, p_value, ground_truth_data_type"


def get_data_point_list_from_directory(path, limit=0):
    files = os.listdir(path)
    data_points = []
    for f in files:
        fdata = f.split(".")
        # Only support JSON data
        if fdata[-1] != "json":
            continue
        cohort = fdata[0]
        dps = get_data_point_list_from_file(f"{path}/{f}", cohort)
        for dp in dps:
            data_points.append(dp)
    if limit > 0:
        dps = dps[0:limit]
    return dps



def get_data_point_list_from_file(path, cohort=""):
    return DataPoint.factory(path, cohort)


def analysis_report_location(predictor_name, data_type):
    return f"/common/yesselmanlab/ewhiting/reports/{predictor_name}_{data_type}_pipeline_report.txt"

def pipeline_report_location(predictor_name, data_type):
    return f"/common/yesselmanlab/ewhiting/reports/{predictor_name}_{data_type}_pipeline.txt"

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

    about_data += f"\nSkipped {skipped_count} molecules due to exceptions\n"

    about_data += f"\nMXFold Performance:\n"
    about_data += f"Average DSCI accuracy score: {round(avg_acc, 4)}\n"
    about_data += f"Average DSCI p-vale score: {avg_p}\n"
    about_data += f"Mode accuracy: {mode_acc}\n"
    about_data += f"Number of DSCI 1.0 scores: {one_point_oh_accuracies}\n"
    about_data += f"Lowest DSCI accruracy score: {lowest_acc[1]} on {lowest_acc[0]}\n"
    about_data += f"Highest DSCI p-value score: {highest_p[1]} on {highest_p[0]}\n"

    about_data += f"\n"
    about_data += f"Report generated on: {datetime.datetime.now()}\n\n"

    f = open(pipeline_report_location(predictor_name, data_type), "w")
    f.write(about_data)
    f.close()

