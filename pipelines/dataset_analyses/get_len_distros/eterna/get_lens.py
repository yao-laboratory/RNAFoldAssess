import os

dataset_dir = "eterna"
data_name = "EternaData"
common = os.getenv("COMMON")
base_path = f"{common}/dataset_analyses/{dataset_dir}"


f = open(f"{base_path}/{data_name}_bad_guesses.txt")
data1 = f.readlines()
f.close()
f = open(f"{base_path}/{data_name}_good_guesses.txt")
data2 = f.readlines()
f.close()

good_lens = []
bad_lens = []

for d in data1:
    length = int(d.split(", ")[-1])
    bad_lens.append(length)

for d in data2:
    length = int(d.split(", ")[-1])
    good_lens.append(length)


gavg = sum(good_lens) / len(good_lens)
bavg = sum(bad_lens) / len(bad_lens)
print(f"Good average: {gavg}")
print(f"Bad average: {bavg}")

import matplotlib.pyplot as plt

n_bins = 20
fig, axs = plt.subplots(1, 2, sharey=False, tight_layout=True)
axs[0].hist(bad_lens, bins=n_bins)
axs[0].set_title("Length distribution of bad predictions")
axs[1].hist(good_lens, bins=n_bins)
axs[1].set_title("Length distribution of good predictions")
plt.savefig(f"{data_name}_legnth_dist.pdf", format="pdf", bbox_inches="tight")

