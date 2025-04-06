import vienna


base_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions"
pred_file = f"{base_dir}/bprna_matched_set_1.txt"

with open(pred_file) as fh:
    predictions = [d.split(", ") for d in fh.readlines()]

seq_index = 3
len_pred = len(predictions)
counter = 0
with open(f"{base_dir}/bprna_matched_1_with_mfe_ed.txt", "w") as fh:
    for pred in predictions:
        pred = [p.strip() for p in pred]
        counter += 1
        if counter % 5000 == 0:
            print(f"Working {counter} of {len_pred}")
        seq = pred[seq_index]
        fold_results = vienna.fold(seq)
        mfe = fold_results.mfe
        ensemble_defect = fold_results.ens_defect
        new_line = ", ".join(pred + [str(mfe), str(ensemble_defect)]) + "\n"
        fh.write(new_line)




