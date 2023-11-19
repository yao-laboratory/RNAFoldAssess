import os, datetime

from RNAFoldAssess.models import DataPointFromCrystal
from RNAFoldAssess.models.predictors import *
from RNAFoldAssess.models.scorers import *

crystal_base = "/common/yesselmanlab/ewhiting/data/crystal2/rna_only/structures/symmetric_structures.txt"

dps = DataPointFromCrystal.factory(crystal_base)
for dp in dps:
    if len(dp.sequence) < 20:
        dps.remove(dp)

# For testing
# dps = dps[175:200]

headers = "algo_name, datapoint_name, lenience, sensitivity, ppv, F1, ground_truth_data_type"
leniences = [0, 1]

# MXFold
model = MXFold()
model_path = os.path.abspath("/home/yesselmanlab/ewhiting/mxfold/build/mxfold")

predictor_name = "MXFold"
data_type = "Crystal2-RNA-Only"

lengths = []
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


analysis_report_path = f"/common/yesselmanlab/ewhiting/reports/rna_only_{predictor_name}_{data_type}_seq20plus_report.txt"
pipeline_report_path = f"/common/yesselmanlab/ewhiting/reports/rna_only_{predictor_name}_{data_type}_seq20plus.txt"

f = open(analysis_report_path, "w")
f.write(f"{headers}\n")

counter = 0
skipped = 0
ss_skipped = 0
dp_size = len(dps)

print("About to run evaluation")
for dp in dps:
    if len(dp.sequence) == 0:
        skipped += 1
        continue
    if len(dp.true_structure) == 0:
        ss_skipped += 1
        continue
    if counter % 125 == 0:
        print(f"Completed {counter} of {dp_size} data points and {len(leniences)} leniences")
    lengths.append(len(dp.sequence))
    input_file_path = dp.to_fasta_file()
    model.execute(model_path, input_file_path)
    prediction = model.get_ss_prediction()
    for lenience in leniences:
        f.write(f"rna_only_{predictor_name}, {dp.name}, {lenience}, ")
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

avg_seq_len = sum(lengths) / len(lengths)

about_data = ""
about_data += f"About {data_type} dataset\n"
about_data += f"Datapoints evaluated: {len(lengths)}\n"
about_data += f"Longest sequence: {max(lengths)}\n"
about_data += f"Shortest sequence: {min(lengths)}\n"
about_data += f"Most common lenth length: {max(set(lengths), key=lengths.count)}\n"
about_data += f"Skipped {skipped} datapoints because they had no sequence\n"
about_data += f"Skipped {ss_skipped} datapoints because they had no secondary structure\n"
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

