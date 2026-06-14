import os

import pandas as pd


base_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions"

files = {
    "easy": f"{base_dir}/chem_map_easy_mfe_ed_master.csv",
    "hard": f"{base_dir}/chem_map_hard_mfe_ed_master.csv"
}

for kind, loc in files.items():
    df = pd.read_csv(loc, index_col=False)

    cols = ["datapoint", "sequence", "length", "gc_content", "mfe", "ens_def"]
    new_df = df[cols]

    new_df.to_csv(f"chem_map_{kind}_filtered.csv", index=False)

print("Done :)")

