import os

from RNAFoldAssess.utils.secondary_structure_tools import SecondaryStructureTools


base_dir = "/common/yesselmanlab/ewhiting/reports/ydata/analyses"
good_guesses_path = f"{base_dir}/all_good_guesses.txt"
bad_guesses_path = f"{base_dir}/all_bad_guesses.txt"

gg_energy_path = f"{base_dir}/good_guesses_with_energy.txt"
bg_energy_path = f"{base_dir}/bad_guesses_with_energy.txt"

good_guesses_file = open(good_guesses_path)
good_guesses = good_guesses_file.readlines()
good_guesses_file.close()
bad_guesses_file = open(bad_guesses_path)
bad_guesses = bad_guesses_file.readlines()
bad_guesses_file.close()

g_fe = []
f_gg = open(gg_energy_path, "w")
for gg in good_guesses:
    d = gg.strip().split(", ")
    seq = d[2]
    stc = d[3]
    fe = SecondaryStructureTools.get_free_energy(seq, stc)
    g_fe.append(fe)
    line = ", ".join(d) + f", {fe}\n"
    f_gg.write(line)
f_gg.close()

b_fe = []
f_bg = open(bg_energy_path, "w")
for bg in bad_guesses:
    d = bg.strip().split(", ")
    seq = d[2]
    stc = d[3]
    fe = SecondaryStructureTools.get_free_energy(seq, stc)
    b_fe.append(fe)
    line = ", ".join(d) + f", {fe}\n"
    b_gg.write(line)
b_gg.close()


import matplotlib.pyplot as plt

n_bins = 20
fig, axs = plt.subplots(1, 2, sharey=False, tight_layout=True)
axs[0].hist(b_fe, bins=n_bins)
axs[0].set_title("Energy distribution of bad predictions")
axs[1].hist(g_fe, bins=n_bins)
axs[1].set_title("Energy distribution of good predictions")
plt.savefig(f"ydata_energy_dist.pdf", format="pdf", bbox_inches="tight")

