import os

import seaborn as sns
import matplotlib.pyplot as plt


dataset_name = "Eterna"
base_dir = "/common/yesselmanlab/ewhiting/reports/eterna_data/ranked"
hi_preds_file = open(f"{base_dir}/EternaData_good_predictions.txt")
lo_preds_file = open(f"{base_dir}/EternaData_bad_predictions.txt")

hi_preds = hi_preds_file.readlines()
lo_preds = lo_preds_file.readlines()

hi_preds_file.close()
lo_preds_file.close()


def get_fe_and_len_data(data):
    fes = []
    lens = []
    gc_contents = []
    for d in data:
        d = d.strip().split(", ")
        fe = float(d[-1])
        seq = d[2]
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

hi_fes, hi_lens, hi_gc = get_fe_and_len_data(hi_preds)
lo_fes, lo_lens, lo_gc = get_fe_and_len_data(lo_preds)

# Remove any free energies larger than 100
len_hi_fes = len(hi_fes)
len_lo_fes = len(lo_fes)
hi_fes = [h for h in hi_fes if h < 100]
lo_fes = [l for l in lo_fes if l < 100]
new_len_hi_fes = len(hi_fes)
new_len_lo_fes = len(lo_fes)

report = f"{dataset_name} predictions analysis report\n"
report += f"Removed {len_hi_fes - new_len_hi_fes} free-energy readings from high-accuracy predictions\nRemoved {len_lo_fes - new_len_lo_fes} free-energy readings from low-accuracy predictions\n"
report_file = open("Free_Energy_and_Lengths_report.txt", "w")
report_file.write(report)

sns.kdeplot(data={"Low Scoring": lo_fes, "High scoring": hi_fes}, legend=True, gridsize=400)
plt.title(f"MFE Dist. in {dataset_name} predictions")
plt.savefig(fname=f"{dataset_name}_FE_DensityPlot.jpg", format="jpg")
plt.clf()

sns.kdeplot(data={"Low Scoring": lo_lens, "High scoring": hi_lens}, legend=True, gridsize=400)
plt.title(f"Length Dist. in {dataset_name} predictions")
plt.savefig(fname=f"{dataset_name}_length_DensityPlot.jpg", format="jpg")
plt.clf()

sns.kdeplot(data={"Low Scoring": lo_gc, "High scoring": hi_gc}, legend=True, gridsize=400)
plt.title(f"GC-Content Dist. in {dataset_name} predictions")
plt.savefig(fname=f"{dataset_name}_GC_DensityPlot.jpg", format="jpg")
plt.clf()

