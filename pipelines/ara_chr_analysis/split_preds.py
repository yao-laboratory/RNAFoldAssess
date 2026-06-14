import os


base_path = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions"
report_file = f"{base_path}/all_rasp_arabidopsis_preds.txt"

def get_chromosome(dp_name):
    ch = dp_name.split("_")[0]
    return ch

with open(report_file) as fh:
    data = [line.split(", ") for line in fh.readlines()]

models = set()
chromosomes = set()
for d in data:
    model = d[0]
    models.add(model)
    chromosome = get_chromosome(d[1])
    chromosomes.add(chromosome)


ch_model_map = {}
for ch in chromosomes:
    ch_model_map[ch] = {}
    for m in models:
        ch_model_map[ch][m] = []


for d in data:
    model = d[0]
    ch = get_chromosome(d[1])
    acc = float(d[4])
    ch_model_map[ch][model].append(acc)


# for ch in chromosomes:
#     print(f"For Chromosome {ch}:")
    
#     # Collect (model, avg_accuracy, n) tuples
#     model_stats = []
#     for m in models:
#         accs = ch_model_map[ch][m]
#         n = len(accs)
#         if n == 0:
#             continue
#         avg = sum(accs) / n
#         model_stats.append((m, avg, n))
    
#     # Sort by average accuracy descending
#     model_stats.sort(key=lambda x: x[1], reverse=True)
    
#     # Print results
#     for m, avg, n in model_stats:
#         print(f"\t{m}: {avg:.4f}, n = {n}")

fstring = ""
models = list(models)
models.sort()
chromosomes = list(chromosomes)
chromosomes.sort()
fstring += ",".join(chromosomes) + '\n'

for m in models:
    fstring += f"{m},"
    accs = []
    for ch in chromosomes:
        ch_accs = ch_model_map[ch][m]
        if len(ch_accs) == 0:
            avg = "None"
        else:
            avg = sum(ch_accs) / len(ch_accs)
        accs.append(avg)
    fstring += ",".join([str(acc) for acc in accs]) + "\n"

with open("ara_model_perf.txt", "w") as fh:
    fh.write(fstring)



import matplotlib.pyplot as plt
import numpy as np

# Models to include
selected_models = ["SPOT-RNA", "IPKnot", "EternaFold"]

# Prepare data
chromosomes = list(ch_model_map.keys())
chromosomes.sort()  # optional, to order chromosomes numerically/alphabetically

# Build average accuracy matrix
avg_acc_matrix = {model: [] for model in selected_models}

for ch in chromosomes:
    for model in selected_models:
        accs = ch_model_map[ch].get(model, [])
        if accs:
            avg = sum(accs) / len(accs)
        else:
            avg = 0
        avg_acc_matrix[model].append(avg)

# Define colors
colors = {
    "SPOT-RNA": "#4E79A7",     # muted blue
    "IPKnot": "#F28E2B",       # muted orange
    "EternaFold": "#76B7B2"    # muted teal
}

# Plotting
x = np.arange(len(chromosomes))
bar_width = 0.25
fig, ax = plt.subplots(figsize=(12, 6))

for i, model in enumerate(selected_models):
    ax.bar(x + i * bar_width, avg_acc_matrix[model],
           width=bar_width,
           label=model,
           color=colors[model])

ax.set_xticks(x + bar_width)
ax.set_xticklabels(chromosomes, rotation=45)
ax.set_xlabel("Chromosome")
ax.set_ylabel("Average Accuracy")
ax.set_title("Model Performance Across Chromosomes")
ax.legend()

plt.tight_layout()
plt.savefig("model_performance_across_chromosomes.png", dpi=300)
plt.close()




print("\nDone")
