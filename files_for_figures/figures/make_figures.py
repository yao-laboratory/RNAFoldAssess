import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

all_files = [f for f in os.listdir("..") if f.endswith(".txt")]

palette = ["#FFBE0B", "#FB5607", "#FF006E", "#8338EC", "#3A86FF"]

def get_color(filename):
    if "eterna" in filename:
        return palette[0]
    if "pri_miRNA" in filename:
        return palette[1]
    if "human_mRNA" in filename:
        return palette[2]
    if "ribo" in filename:
        return palette[3]
    if "ydata" in filename:
        return palette[4]


ordered_by_type = {
    "Experimental": ["ContextFold", "ContraFold", "EternaFold", "RandomPredictor", "IPKnot", "NeuralFold"],
    "Physics": ["NUPACK", "RNAFold", "RNAStructure", "pKnots", "Simfold"],
    "MachineLearning": ["MXFold", "MXFold2", "SPOT-RNA"]
}

for ff in all_files:
    try:
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

        # Create a figure and axis
        plt.figure(figsize=(8, 4))  # Adjust the figure size as needed
        ax = sns.violinplot(
            x=data,
            orient='h',
            color=get_color(ff),
            inner=None,
            cut=0,
        )  # Horizontal orientation

        # # Calculate median
        # median_value = np.median(data)

        # # Overlay a circle at the median
        # ax.scatter(median_value, 0, color='white', s=100, marker='o', zorder=3)  # Adjust size and color as needed

        # Remove tick marks and labels
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xticklabels([])
        ax.set_yticklabels([])

        # Optionally, remove the axis frame
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)

        # Optionally, remove the grid
        ax.grid(False)

        # Overlay the box plot
        sns.boxplot(
            ax=ax,
            x=data,
            orient='h',
            boxprops=dict(facecolor='red', color='black'),
            width=0.5,  # Adjust the width of the box plot as needed
            fliersize=0,  # To hide any outlier points
        )

        # Save the figure
        plt.savefig(f'{model_name}_{data_name}.jpeg', format='jpeg', bbox_inches='tight', pad_inches=0)
        plt.close()  # Close the figure to avoid display in some environments

    except Exception as e:
        print(f"{ff} --> {e}")
        continue

