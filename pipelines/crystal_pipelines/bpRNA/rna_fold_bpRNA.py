import os, datetime

from RNAFoldAssess.models.predictors import *
from RNAFoldAssess.models.scorers import *

model_name = "RNAFold"
model = RNAFold()
model_path = os.path.abspath("/home/yesselmanlab/ewhiting/ViennaRNA/bin/RNAfold")
data_type_name = "bpRNA-1m-90"
headers = "algo_name, datapoint_name, lenience, sensitivity, ppv, F1, data_point_type"
leniences = []
skipped = 0

# Let's make the files first and see if that makes the process faster
fasta_path = "/common/yesselmanlab/ewhiting/data/bprna/fasta_files"
# RNAFold needs a fasta file
def sequence_to_file(name, sequence):
    name = name.replace(" ", "_")
    name = name.replace("/", "")
    name = name.replace("'", "")
    name = name.replace("(", "")
    name = name.replace(")", "")
    name = name.replace("[", "")
    name = name.replace("]", "")
    name = name.replace("{", "")
    name = name.replace("}", "")
    name = name.replace("<", "")
    name = name.replace(">", "")
    name = name.replace(";", "")
    name = name.replace(",", "")
    name = name.replace("|", "")
    name = name.replace("`", "")
    name = name.replace('"', "")
    name = name.replace("$", "S")
    name = name.replace("&", "and")
    name = name.replace("~", "")
    if len(name) > 200:
        name = name[0:200]
    fasta_string = f">{name} en=0.00\n{sequence}\n"
    f = open(f"{fasta_path}/{name}.fasta", "w")
    f.write(fasta_string)
    f.close()

dbn_path = "/common/yesselmanlab/ewhiting/data/bprna/dbnFiles"
files = os.listdir(dbn_path)
file_len = len(files)

# counter = 0
# for file in files:
#     if counter % 250 == 0:
#         print(f"Completed {counter} of {file_len}")
#     dbn_file = open(f"{dbn_path}/{file}")
#     data = dbn_file.readlines()
#     dbn_file.close()
#     if len(data) != 5:
#         print(f"Skipping {file} for weird file format")
#         skipped += 1
#     name = data[0].split("#Name: ")[1].strip()
#     sequence = data[3].strip()
#     sequence_to_file(name, sequence)
#     counter += 1


# process the data


lengths = []
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

counter = 0
fasta_files = os.listdir(fasta_path)

analysis_report_path = f"/common/yesselmanlab/ewhiting/reports/{model_name}_{data_type_name}_report.txt"
pipeline_report_path = f"/common/yesselmanlab/ewhiting/reports/{model_name}_{data_type_name}.txt"

# For testing
# fasta_files = fasta_files[0:5]

f = open(analysis_report_path, "w")
f.write(f"{headers}\n")
for fasta_file in fasta_files:
    if counter % 250 == 0:
        print(f"Completed {counter} of {file_len}")
    name = fasta_file.split(".")[0]
    data_type = name.split("_")[1]
    dbn_file_path = f"{dbn_path}/{name}.dbn"
    # e.g. bpRNA_CRW_49455.dbn
    dbn_file = open(dbn_file_path)
    data = dbn_file.readlines()
    true_structure = data[4].strip()
    lengths.append(len(true_structure))
    dbn_file.close()
    try:
        model.execute(model_path, f"{fasta_path}/{fasta_file}")
        prediction = model.get_ss_prediction()
        for lenience in leniences:
            f.write(f"{model_name}, {name}, {lenience}, ")
            scorer = BasePairScorer(true_structure, prediction, lenience)
            scorer.evaluate()
            s = scorer.sensitivity
            p = scorer.ppv
            f1 = scorer.f1
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

            f.write(f"{s}, {p}, {f1}\n")
        counter += 1
    except:
        skipped += 1
        continue

    f.close()

avg_seq_len = sum(lengths) / len(lengths)

about_data = ""
about_data += f"About {data_type} dataset\n"
about_data += f"Datapoints evaluated: {len(lengths)}\n"
about_data += f"Longest sequence: {max(lengths)}\n"
about_data += f"Shortest sequence: {min(lengths)}\n"
about_data += f"Most common lenth length: {max(set(lengths), key=lengths.count)}\n"
about_data += f"Skipped {skipped} datapoints because they had no sequence\n"
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



