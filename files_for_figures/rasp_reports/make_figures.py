import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


algorithm_colors = {
    "ContextFold": "#1f77b4",
    "ContraFold": "#ff7f0e",
    "EternaFold": "#2ca02c",
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


models = list(algorithm_colors.keys())

species = [
    "cov",
    "ecoli",
    "hiv",
    # "human",
    # "arabidopsis"
]


for s in species:
    all_data = {}
    for m in models:
        with open(f"{m}_{s}_accs.txt") as acc_file:
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
    plt.savefig(f"figures/{s}_rasp_predictions.jpeg", format="jpeg", bbox_inches="tight", pad_inches=0)
