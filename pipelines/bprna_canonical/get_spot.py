import os

from RNAFoldAssess.models.scorers import CanonicalBasePairScorer


base_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions"

seq_index = 4
tru_index = 5
pred_index = 6

new_report_path = "/work/yesselmanlab/ewhiting/bprna_canonical_reports"

print("Building inex")
dp_index_path = "/work/yesselmanlab/ewhiting/data/bprna/dp_index.txt"
with open(dp_index_path) as fh:
    dp_data = [line.strip().split(" ") for line in fh.readlines()]

dp_index = {}
for seq, dp in dp_data:
    dp_index[seq] = dp

for lenience in [0, 1]:
    print(f"Working {lenience} lenience")
    fname = f"{base_dir}/bprna_master_file_{lenience}.txt"
    with open(fname) as fh:
        data = [line for line in fh.readlines() if "SPOT-RNA" in line]

    data = [d.split(", ") for d in data]
    headers = "model_name, dp_name, lenience, sequence, true_structure, predicted_structure, sensitivity, ppv, f1\n"

    with open(f"{new_report_path}/SPOT-RNA_master_{lenience}_lenience.txt", "w") as fh:
        fh.write(headers)
        for d in data:
            model_name = "SPOT-RNA"
            # lenience_name = d[2]
            seq = d[seq_index]
            stc = d[tru_index]
            pred = d[pred_index]
            dp_name = dp_index[seq]
            new_line = f"{model_name}, {dp_name}, {lenience}, "
            new_line += f"{seq}, {stc}, {pred}, "
            scorer = CanonicalBasePairScorer(seq, stc, pred, lenience)
            scorer.evaluate()
            s = scorer.sensitivity
            p = scorer.ppv
            f1 = scorer.f1
            new_line += f"{s}, {p}, {f1}\n"

            fh.write(new_line)

print("Done")
