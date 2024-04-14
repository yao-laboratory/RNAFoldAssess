import matplotlib.pyplot as plt

base_dir = "/common/yesselmanlab/ewhiting/reports/eterna_data/ranked"
bpath = f"{base_dir}/EternaData_bad_predictions.txt"
gpath = f"{base_dir}/EternaData_good_predictions.txt"

bf = open(bpath)
bdata = bf.readlines()
bf.close()

gf = open(gpath)
gdata = gf.readlines()
gf.close()

bad_energies = []
good_energies = []

for d in gdata:
    d = d.strip()
    fe = float(d.split(", ")[-1])
    good_energies.append(fe)

for d in bdata:
    d = d.strip()
    fe = float(d.split(", ")[-1])
    bad_energies.append(fe)


n_bins = 50
fig, axs = plt.subplots(1, 2, sharey=False, tight_layout=True)
axs[0].hist(bad_energies, bins=n_bins)
axs[0].set_title("Energy distribution of bad predictions")
axs[1].hist(good_energies, bins=n_bins)
axs[1].set_title("Energy distribution of good predictions")
plt.savefig(f"Eterna_energy_dist.pdf", format="pdf", bbox_inches="tight")
