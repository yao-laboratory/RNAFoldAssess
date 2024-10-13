import os

from scipy import stats
from scipy.stats import anderson, kstest
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


all_files = [f for f in os.listdir("..") if f.endswith(".txt")]

ad_result_file = open("anderson_darling.txt", "w")
ks_result_file = open("kolmogorov_smirnov.txt", "w")

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

    ad_result = anderson(data)
    ad_message = f"{model_name} on {data_name}\n"
    ad_message += f"Statistic: {ad_result.statistic}\n"
    ad_message += f"Critical values: {ad_result.critical_values}\n"
    ad_message += f"Significance Level: {ad_result.significance_level}\n"

    # Interpret the result
    if ad_result.statistic < ad_result.critical_values[2]:  # 5% significance level
        ad_message += "The data is normally distributed.\n\n"
    else:
        ad_message += "The data is not normally distributed.\n\n"
    
    ad_result_file.write(ad_message)

    ks_statistic, ks_p_value = kstest(data, 'norm', args=(np.mean(data), np.std(data)))
    ks_message = f"{model_name} on {data_name}\n"
    ks_message += f"KS Statistic: {ks_statistic}, p-value: {ks_p_value}\n"
    alpha = 0.05  # significance level
    if ks_p_value > alpha:
        ks_message += "The data is normally distributed.\n\n"
    else:
        ks_message += "The data is not normally distributed.\n\n"
    ks_result_file.write(ks_message)

    

ad_result_file.close()
ks_result_file.close()
