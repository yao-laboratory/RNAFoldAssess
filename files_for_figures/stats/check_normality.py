import os

from scipy import stats
from scipy.stats import anderson
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


all_files = [f for f in os.listdir("..") if f.endswith(".txt")]

result_file = open("shapiro_wilks_result.txt", "w")

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

    # Create the Q-Q plot
    plt.figure(figsize=(8, 6))
    stats.probplot(data, dist="norm", plot=plt)
    plt.title("Q-Q Plot")
    plt.xlabel("Theoretical Quantiles")
    plt.ylabel("Sample Quantiles")
    plt.grid()
    plt.savefig(f'{model_name}_{data_name}_QQ.jpeg', format='jpeg', bbox_inches='tight', pad_inches=0)
    plt.close()

    # Perform the Shapiro-Wilk test
    shapiro_stat, shapiro_p = stats.shapiro(data)

    # Save the results
    result = f"{model_name} on {data_name}\n"
    result += f"Shapiro-Wilk Test Statistic: {shapiro_stat}\n"
    result += f"Shapiro-Wilk Test p-value: {shapiro_p}\n"

    # Interpret the p-value
    alpha = 0.05  # significance level
    if shapiro_p > alpha:
        result += "Fail to reject the null hypothesis: the data is normally distributed.\n\n"
    else:
        result += "Reject the null hypothesis: the data is not normally distributed.\n\n"

    result_file.write(result)

result_file.close()
