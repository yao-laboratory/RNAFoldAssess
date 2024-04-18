import os

import seaborn as sns
import matplotlib.pyplot as plt

from RNAFoldAssess.utils.secondary_structure_tools import SecondaryStructureTools

dataset_name = "RNAndria"

base_dir = "/common/yesselmanlab/ewhiting/reports/rnandria/analyses"
hi_pred_files = {
    "all": open(f"{base_dir}/all_high_predictions.txt"),
    "pri": open(f"{base_dir}/pri/pri_miRNA_high_predictions.txt"),
    "human": open(f"{base_dir}/human/human_mRNA_high_predictions.txt")
}

lo_pred_files = {
    "all": open(f"{base_dir}/all_low_predictions.txt"),
    "pri": open(f"{base_dir}/pri/pri_miRNA_low_predictions.txt"),
    "human": open(f"{base_dir}/human/human_mRNA_low_predictions.txt")
}

hi_preds = {
    "all": hi_pred_files["all"].readlines(),
    "pri": hi_pred_files["pri"].readlines(),
    "human": hi_pred_files["human"].readlines()
}

lo_preds = {
    "all": lo_pred_files["all"].readlines(),
    "pri": lo_pred_files["pri"].readlines(),
    "human": lo_pred_files["human"].readlines()
}

for files in [hi_pred_files, lo_pred_files]:
    for f in files:
        files[f].close()


def get_fe_and_len_data(data):
    fes = []
    lens = []
    gc_contents = []
    for d in data:
        d = d.strip().split(", ")
        if d[1] == "SeqFold":
            continue
        stc = d[3]
        seq = d[2]
        fe = SecondaryStructureTools.get_free_energy(seq, stc)
        seq_len = len(seq)
        gc_content = get_gc_content(seq)
        fes.append(fe)
        lens.append(seq_len)
        gc_contents.append(gc_content)
    return fes, lens, gc_contents

def get_gc_content(seq):
    seq = seq.strip().upper() # Just in case
    gs = seq.count("G")
    cs = seq.count("C")
    gc_count = gs + cs
    gc_content = gc_count / len(seq)
    if gc_content > 1:
        print(seq)
    return gc_content

for k in hi_preds:
    print(k)
    hi_fes, hi_lens, hi_gc = get_fe_and_len_data(hi_preds[k])
    lo_fes, lo_lens, lo_gc = get_fe_and_len_data(lo_preds[k])
    # Remove any free energies larger than 100
    len_hi_fes = len(hi_fes)
    len_lo_fes = len(lo_fes)
    hi_fes = [h for h in hi_fes if h < 100]
    lo_fes = [l for l in lo_fes if l < 100]
    new_len_hi_fes = len(hi_fes)
    new_len_lo_fes = len(lo_fes)

    report = f"{dataset_name} predictions analysis report\n"
    report += f"Removed {len_hi_fes - new_len_hi_fes} free-energy readings from high-accuracy predictions\nRemoved {len_lo_fes - new_len_lo_fes} free-energy readings from low-accuracy predictions\n"
    report_file = open(f"{k}_free_Energy_and_Lengths_report.txt", "w")
    report_file.write(report)
    report_file.close()

    sns.kdeplot(data={"Low Scoring": lo_fes, "High scoring": hi_fes}, legend=True, gridsize=400)
    plt.title(f"MFE Dist. in {dataset_name} - {k} predictions")
    plt.savefig(fname=f"{dataset_name}_{k}_FE_DensityPlot.jpg", format="jpg")
    plt.clf()

    sns.kdeplot(data={"Low Scoring": lo_lens, "High scoring": hi_lens}, legend=True, gridsize=400)
    plt.title(f"Length Dist. in {dataset_name} - {k} predictions")
    plt.savefig(fname=f"{dataset_name}_{k}_length_DensityPlot.jpg", format="jpg")
    plt.clf()

    sns.kdeplot(data={"Low Scoring": lo_gc, "High scoring": hi_gc}, legend=True, gridsize=400)
    plt.title(f"GC-Content Dist. in {dataset_name} - {k} predictions")
    plt.savefig(fname=f"{dataset_name}_{k}_GC_DensityPlot.jpg", format="jpg")
    plt.clf()

