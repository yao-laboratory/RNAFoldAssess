import os

import pandas as pd
import matplotlib.pyplot as plt


report_dir = "/common/yesselmanlab/ewhiting/reports/ydata/analyses"
gpath = f"{report_dir}/good_guesses_with_energy.txt"
bpath = f"{report_dir}/bad_guesses_with_energy.txt"

gf = open(gpath)
gdata = gf.readlines()
gf.close()
bf = open(bpath)
bdata = bf.readlines()
bf.close()

gdata = [d.strip() for d in gdata]
bdata = [d.strip() for d in bdata]

good_pred_energies = []
bad_pred_energies = []

for d in gdata:
    fe = float(d.split(", ")[-1])
    good_pred_energies.append(fe)

for d in bdata:
    fe = float(d.split(", ")[-1])
    bad_pred_energies.append(fe)

n_bins = 50
fig, axs = plt.subplots(1, 2, sharey=False, tight_layout=True)
axs[0].hist(bad_pred_energies, bins=n_bins)
axs[0].set_title("Free energy of bad predictions")
axs[1].hist(good_pred_energies, bins=n_bins)
axs[1].set_title("Free energy of good predictions")
plt.savefig(f"ydata_energy_dist.pdf", format="pdf", bbox_inches="tight")

