import os

from RNAFoldAssess.models.scorers import BasePairScorer


pred_file_loc = "/work/yesselmanlab/ewhiting/spot_scripts/bprna/ct_files"
dbn_file_loc = "/work/yesselmanlab/ewhiting/data/bprna/dbnFiles_sep"

rf0 = "/work/yesselmanlab/ewhiting/bprna_preds/redo_reports/SPOT-RNA_master_0_lenience.txt"
rf1 = "/work/yesselmanlab/ewhiting/bprna_preds/redo_reports/SPOT-RNA_master_1_lenience.txt"
reports = [open(rf0, "w"), open(rf1, "w")]

headesr = f"model_name, dp_name, lenience, sequence, true_structure, predicted_structure, sensitivity, ppv, f1\n"

for i in range(100):
    print(f"Working part {i}")
    dbn_files = os.listdir(f"{dbn_file_loc}/part_{i}")
    for dbn_file in dbn_files:
        name = dbn_file.split(".")[0]
        with open(f"{dbn_file_loc}/part_{i}/{dbn_file}") as fh:
            dbn_data = fh.readlines()
        seq = dbn_data[3].strip()
        dbn = dbn_data[4].strip()
        try:
            with open(f"{pred_file_loc}/{name}.ct.dbn") as fh:
                pred_data = fh.readlines()
            pred_seq = pred_data[1].strip()
            if pred_seq != seq:
                print(f"Sequence mismatch in {name}")
                continue
            pred = pred_data[2].strip()
            # Just evaluate open and closed parentheses
            new_pred = ""
            new_dbn = ""
            for nt in pred:
                if nt not in "(.)":
                    new_pred += "."
                else:
                    new_pred += nt
            for nt in dbn:
                if nt not in "(.)":
                    new_dbn += "."
                else:
                    new_dbn += nt

            pred = new_pred
            dbn = new_dbn

            for lenience in [0, 1]:
                scorer = BasePairScorer(dbn, pred, lenience)
                scorer.evaluate()
                s = scorer.sensitivity
                p = scorer.ppv
                f1 = scorer.f1
                line_to_write = f"SPOT-RNA, {name}, {lenience}, {seq}, {dbn}, {pred}, "
                line_to_write += f"{s}, {p}, {f1}\n"
                reports[lenience].write(line_to_write)
        except FileNotFoundError:
            continue


for report in reports:
    report.close()
