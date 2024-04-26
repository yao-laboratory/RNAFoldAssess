import os


import matplotlib.pyplot as plt


desc_dir = "/common/yesselmanlab/ewhiting/data/descriptions"

all_files = os.listdir(desc_dir)

ln_files = [f for f in all_files if f.endswith("legnths.txt")]
gc_files = [f for f in all_files if f.endswith("gc_content.txt")]

datasets = [
    "bprna",
    "eterna",
    # "rasp",
    "ribonanza",
    "rnandria",
    "ydata"
]

pretty_names = [
    "bpRNA",
    "Eterna",
    # "RASP",
    "Ribonanza",
    "RNAndria",
    "Yesselman Lab Data"
]

dataset_sizes = {}
lens = {}
gcs = {}

for ds in datasets:
    if ds == "rasp":
        ln_file_name = "rasp_all_lengths.txt"
        gc_file_name = "rasp_all_gc_content.txt"
    elif ds == "rnandria":
        ln_file_name = "rnandria_all_lengths.txt"
        gc_file_name = "rnandria_all_gc_content.txt"
    else:
        ln_file_name = f"{ds}_lengths.txt"
        gc_file_name = f"{ds}_gc_content.txt"

    ln_file = open(f"{desc_dir}/{ln_file_name}")
    gc_file = open(f"{desc_dir}/{gc_file_name}")

    ln_data = ln_file.readlines()
    ln_file.close()
    ln_data = [int(d.strip()) for d in ln_data]
    lens[ds] = ln_data

    gc_data = gc_file.readlines()
    gc_file.close()
    gc_data = [float(d.strip()) for d in gc_data]
    gcs[ds] = gc_data

    dataset_sizes[ds] = len(gc_data)


f = open(f"{desc_dir}/dataset_sizes.txt", "w")
for s in dataset_sizes:
    f.write(f"{s}: {dataset_sizes[s]}\n")
f.close()

all_len_data = []
for s in lens:
    all_len_data.append(lens[s])

fig = plt.figure(figsize =(10, 7))
ax = fig.add_subplot(111)

bp = ax.boxplot(all_len_data, patch_artist = True, vert = 0)

for p in bp["boxes"]:
    p.set_facecolor("#7393B3")

for whisker in bp['whiskers']:
    whisker.set(color ='#000000', linewidth = 1.5, linestyle =":")

ax.set_yticklabels(pretty_names)
plt.title("Sequence Lengths")

plt.savefig(fname="sequence_lengths.jpg", format="jpg")

plt.clf()

all_gc_data = []
for s in gcs:
    all_gc_data.append(gcs[s])

fig = plt.figure(figsize =(10, 7))
ax = fig.add_subplot(111)

bp = ax.boxplot(all_gc_data, patch_artist = True, vert = 0)

for p in bp["boxes"]:
    p.set_facecolor("#7393B3")

for whisker in bp['whiskers']:
    whisker.set(color ='#000000', linewidth = 1.5, linestyle =":")

ax.set_yticklabels(pretty_names)
plt.title("Sequence GC Content")

plt.savefig(fname="sequence_gc_content.jpg", format="jpg")

plt.clf()
