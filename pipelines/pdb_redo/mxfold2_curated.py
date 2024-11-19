import ast


from RNAFoldAssess.models.predictors import *
from RNAFoldAssess.models.scorers import *


model = MXFold2RetrainedCurated()
model_name = "MXFold2RetrainedCurated"

def make_prediction(sequence, actual_bps, lenience, file_path=""):
    model.execute(file_path)
    predicted_structure = model.get_ss_prediction()
    score = BasePairScorer.score_from_given_bps(predicted_structure, actual_bps, lenience, list_is_1_indexed=True)
    s  = score["sensitivity"]
    p  = score["ppv"]
    f1 = score["f1"]
    bp_str_rep = ""
    for bp in actual_bps:
        bp_str_rep += f"{bp[0]}-{bp[1]};"
    score_report = f"{bp_str_rep}, {predicted_structure}, {s}, {p}, {f1}\n"
    return score_report

def make_fasta(sequence, name):
    with open(f"/scratch/{name}.fasta", "w") as fh:
        fh.write(f">{name}\n{sequence}")
    return f"/scratch/{name}.fasta"


csv_loc = "/common/yesselmanlab/ewhiting/data/pdb_from_github/PDB-RNA.csv"
with open(csv_loc) as fh:
    data = fh.readlines()
data.pop(0)

report_loc = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/pdb_redo"
rfiles = [
    open(f"{report_loc}/{model_name}_0_lenience_report.txt", "w"),
    open(f"{report_loc}/{model_name}_1_lenience_report.txt", "w")
]

len_data = len(data)
counter = 0
for d in data:
    counter += 1
    if counter % 50 == 0:
        print(f"Working {counter} of {len_data}")
    if "[]" not in d:
        bp_start = d.find('"[[')
        bp_end = d.find(']]"')
        bps = d[bp_start:bp_end+3]
        bps = ast.literal_eval(bps.replace('"', ""))
    name = d.split(",")[0]
    seq = d.split(",")[1]
    fasta_file = make_fasta(seq, name)
    for lenience in [0, 1]:
        pred_string = make_prediction(seq, bps, lenience, file_path=fasta_file)
        line_to_write = f"PDB, {model_name}, {name}, {lenience}, {seq}, {pred_string}"
        rfiles[lenience].write(line_to_write)



for f in rfiles:
    f.close()
