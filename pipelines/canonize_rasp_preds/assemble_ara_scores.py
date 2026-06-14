base_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/consolidated"
files = [
    "RASP_ara_canonical_preds_no_score_1.txt",
    "RASP_ara_canonical_preds_no_score_2.txt",
    "RASP_ara_canonical_preds_no_score_3.txt",
    "RASP_ara_canonical_preds_no_score_4.txt"
]

dest_file = open(f"RASP_ara_canonical_preds_no_score.txt", "w")

for f in files:
    with open(f"{base_dir}/{f}") as fh:
        dest_file.write(fh.read())

dest_file.close()

print("Done")
