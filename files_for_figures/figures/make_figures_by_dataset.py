import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

all_files = [f for f in os.listdir("..") if f.endswith(".txt")]

datset_colors = {
    "eterna": "#5F0F40",
    "pri_miRNA": "#9A031E",
    "human_mRNA": "#FB8B24",
    "ribo": "#E36414",
    "ydata": "#0F4C5C"
}

algorithm_colors = {
    "ContextFold": "#1f77b4",
    "ContraFold": "#ff7f0e",
    "EternaFold": "#2ca02c",
    "RandomPredictor": "#d62728",
    "IPKnot": "#9467bd",
    "NeuralFold": "#8c564b",
    "NUPACK": "#e377c2",
    "RNAFold": "#7f7f7f",
    "RNAStructure": "#bcbd22",
    "pKnots": "#17becf",
    "Simfold": "#ffbb78",
    "MXFold": "#98df8a",
    "MXFold2": "#c49c94",
    "SPOT-RNA": "#f7b6d2"
}

ordered_by_type = {
    "Experimental": ["ContextFold", "ContraFold", "EternaFold", "RandomPredictor", "IPKnot", "NeuralFold"],
    "Physics": ["NUPACK", "RNAFold", "RNAStructure", "pKnots", "Simfold"],
    "MachineLearning": ["MXFold", "MXFold2", "SPOT-RNA"]
}

# List of model names
models = list(algorithm_colors.keys())  # This ensures you're using the models from the colors dict

# Do eterna
all_data = {}
for m in models:
    with open(f"../{m}_eterna_accuracies.txt") as acc_file:
        data = [float(d) for d in acc_file.read().split(",")]
        all_data[m] = data

# Create a figure and axes for the violin plots
fig, ax = plt.subplots(len(models), 1, figsize=(8, len(models) * 2), sharex=True)

# Plot each model's accuracies as a horizontal violin plot
for i, (model, data) in enumerate(all_data.items()):
    sns.violinplot(data=data, ax=ax[i], orient='h', color=algorithm_colors[model], cut=0)

    # Set the label for each plot to the model name
    ax[i].set_ylabel(model)

# Adjust the layout to make space for the labels
plt.tight_layout()
plt.savefig(f"Eterna_Data_predictions.jpeg", format="jpeg", bbox_inches="tight", pad_inches=0)

