import os

from scipy.stats import kruskal


all_files = [f for f in os.listdir("..") if f.endswith(".txt")]

divided_data = {}
for ff in all_files:
    name = ff.replace(".txt", "")
    name = name.replace("_accuracies", "")
    underscore_index = name.find("_")
    model_name = name[:underscore_index]
    data_name = name[underscore_index+1:]  # Plus one to get rid of the underscore

    with open(f"../{ff}") as fh:
        data = fh.read()

    if len(data) == 0:
        continue

    data = [float(d) for d in data.split(",")]
    try:
        divided_data[data_name].append(data)
    except KeyError:
        divided_data[data_name] = [data]


for dataset in divided_data:
    f = open(f"kruskal_results/{dataset}_kruskal.txt", "w")
    values = divided_data[dataset]
    stat, p = kruskal(*values)
    alpha = 0.05  # significance level
    result_message = f"Kruskal H-test on {dataset} predictions\n"
    result_message += f"Statistic: {stat:.4f}\n"
    result_message += f"p-value: {p:.4f}\n"
    if p > alpha:
        result_message += "Fail to reject the null hypothesis: the groups are likely from the same distribution.\n"
    else:
        result_message += "Reject the null hypothesis: at least one group is different.\n"

    f.write(result_message)
    f.close()

