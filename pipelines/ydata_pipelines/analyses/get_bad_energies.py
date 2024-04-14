import os

from RNAFoldAssess.utils.secondary_structure_tools import SecondaryStructureTools


base_dir = "/common/yesselmanlab/ewhiting/reports/ydata/analyses"
bad_guesses_path = f"{base_dir}/all_bad_guesses.txt"

bg_energy_path = f"{base_dir}/bad_guesses_with_energy.txt"

bad_guesses_file = open(bad_guesses_path)
bad_guesses = bad_guesses_file.readlines()
bad_guesses_file.close()

f_bg = open(bg_energy_path, "w")
bg_len = len(bad_guesses)
counter = 0
for bg in bad_guesses:
    d = bg.strip().split(", ")
    seq = d[2]
    stc = d[3]
    fe = SecondaryStructureTools.get_free_energy(seq, stc)
    line = ", ".join(d) + f", {fe}\n"
    f_bg.write(line)
    counter += 1
    if counter % 200 == 0:
      print(f"Finished {counter} of {bg_len}")

f_bg.close()


# import matplotlib.pyplot as plt

# n_bins = 20
# fig, axs = plt.subplots(1, 2, sharey=False, tight_layout=True)
# axs[0].hist(b_fe, bins=n_bins)
# axs[0].set_title("Energy distribution of bad predictions")
# axs[1].hist(g_fe, bins=n_bins)
# axs[1].set_title("Energy distribution of good predictions")
# plt.savefig(f"ydata_energy_dist.pdf", format="pdf", bbox_inches="tight")

