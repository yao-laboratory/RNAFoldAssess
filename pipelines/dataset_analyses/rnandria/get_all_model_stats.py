import os

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


base_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/rnandria"

data_types = ["human_mRNA", "pri_miRNA"]
models = [
    "ContextFold",
    "ContraFold",
    "EternaFold",
    "IPKnot",
    "MXFold",
    "MXFold2",
    "NeuralFold",
    "NUPACK",
    "pKnots",
    "RandomPredictor",
    "RNAFold",
    "RNAStructure",
    "Simfold",
    "SPOT-RNA"
]

pred_accs = {}

for dt in data_types:
    pred_accs[dt] = {}
    for m in models:
        pred_accs[dt][m] = []


for dt in data_types:
    for m in models:
        with open(f"/mnt/nrdstor/yesselmanlab/ewhiting/reports/rnandria/{m}_rnandria_{dt}_predictions.txt") as f:
            data = [d.split(", ") for d in f.readlines()]
        try:
            pred_accs[dt][m] = [float(d[4]) for d in data if len(d) > 3]
            print(f"{dt} - {m}: {len(pred_accs[dt][m])}")
        except Exception as e:
            print(f"Problem in {dt} - {m}: {e}")
        

# Rename "RandomPredictor"
for dt in data_types:
    sampling = pred_accs[dt]["RandomPredictor"]
    del(pred_accs[dt]["RandomPredictor"])
    pred_accs[dt]["EternaSampling"] = sampling

def create_violin_plot(data, title, filename):
    # Convert data to Pandas DataFrame
    df = pd.DataFrame({k: pd.Series(v) for k, v in data.items()})
    
    # Melt the DataFrame to "long-form" for seaborn plotting
    df_melted = df.melt(var_name='Model', value_name='Prediction Accuracy')
    
    # Create the violin plot
    plt.figure(figsize=(10, 6))
    sns.violinplot(x='Model', y='Prediction Accuracy', data=df_melted)
    plt.title(title)
    plt.ylabel('Prediction Accuracy')
    plt.xlabel('Model')
    plt.xticks(rotation=45)
    
    # Save the plot to a file
    plt.savefig(filename, format='jpeg')
    plt.close()


# create_violin_plot(pred_accs['pri_miRNA'], 'Prediction Accuracies for pri_miRNA', 'pri_miRNA_violin_plot.jpeg')
# create_violin_plot(pred_accs['human_mRNA'], 'Prediction Accuracies for human_mRNA', 'human_mRNA_violin_plot.jpeg')

def create_box_plot(data, title, filename):
    # Convert data to Pandas DataFrame
    df = pd.DataFrame({k: pd.Series(v) for k, v in data.items()})
    
    # Melt the DataFrame to "long-form" for seaborn plotting
    df_melted = df.melt(var_name='Model', value_name='Prediction Accuracy')
    
    # Create the box plot
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='Model', y='Prediction Accuracy', data=df_melted, color="g")
    plt.title(title)
    plt.ylabel('Prediction Accuracy')
    plt.xlabel('Model')
    
    # Rotate x-axis labels
    plt.xticks(rotation=45)
    
    # Save the plot to a file
    plt.savefig(filename, format='jpeg')
    plt.close()


# create_box_plot(pred_accs['pri_miRNA'], 'Prediction Accuracies for pri_miRNA', 'pri_miRNA_box_plot.jpeg')
# create_box_plot(pred_accs['human_mRNA'], 'Prediction Accuracies for human_mRNA', 'human_mRNA_box_plot.jpeg')

def create_heatmap(data, title, filename):
    df = pd.DataFrame({k: pd.Series(v) for k,v in data.items()})
    df_melted = df.melt(var_name="Model", value_name="Prediction Accuracy")
    plt.figure(figsize=(10, 6))
    sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
    plt.title(title)
    plt.ylabel('Prediction Accuracy')
    plt.xlabel('Model')
    
    # Rotate x-axis labels
    plt.xticks(rotation=45)
    
    # Save the plot to a file
    plt.savefig(filename, format='jpeg')
    plt.close()


# create_heatmap(pred_accs['pri_miRNA'], 'Prediction Accuracies for pri_miRNA', 'pri_miRNA_heatmap.jpeg')
# create_heatmap(pred_accs['human_mRNA'], 'Prediction Accuracies for human_mRNA', 'human_mRNA_heatmap.jpeg')

def create_facet_grd(data, title, filename):
    df = pd.DataFrame({k: pd.Series(v) for k,v in data.items()})
    df_melted = df.melt(var_name="Model", value_name="Prediction Accuracy")
    plt.figure(figsize=(10, 6))
    g = sns.FacetGrid(df_melted, col='Model', col_wrap=4)
    g.map(sns.histplot, 'Prediction Accuracy')
    plt.title(title)
    plt.ylabel('Prediction Accuracy')
    plt.xlabel('Model')
    
    # Rotate x-axis labels
    plt.xticks(rotation=45)
    
    # Save the plot to a file
    plt.savefig(filename, format='jpeg')
    plt.close()

# create_facet_grd(pred_accs['pri_miRNA'], 'Prediction Accuracies for pri_miRNA', 'pri_miRNA_facet_grid.jpeg')
# create_facet_grd(pred_accs['human_mRNA'], 'Prediction Accuracies for human_mRNA', 'human_mRNA_facet_grid.jpeg')

def create_swarm_plot(data, title, filename):
    df = pd.DataFrame({k: pd.Series(v) for k,v in data.items()})
    df_melted = df.melt(var_name="Model", value_name="Prediction Accuracy")
    plt.figure(figsize=(10, 6))
    sns.swarmplot(x='Model', y='Prediction Accuracy', data=df_melted)
    plt.title(title)
    plt.ylabel('Prediction Accuracy')
    plt.xlabel('Model')
    
    # Rotate x-axis labels
    plt.xticks(rotation=45)
    
    # Save the plot to a file
    plt.savefig(filename, format='jpeg')
    plt.close()

create_swarm_plot(pred_accs['pri_miRNA'], 'Prediction Accuracies for pri_miRNA', 'pri_miRNA_swarm_plot.jpeg')
create_swarm_plot(pred_accs['human_mRNA'], 'Prediction Accuracies for human_mRNA', 'human_mRNA_swarm_plot.jpeg')


def create_strip_plot(data, title, filename):
    df = pd.DataFrame({k: pd.Series(v) for k,v in data.items()})
    df_melted = df.melt(var_name="Model", value_name="Prediction Accuracy")
    plt.figure(figsize=(10, 6))
    sns.stripplot(x='Model', y='Prediction Accuracy', data=df_melted)
    plt.title(title)
    plt.ylabel('Prediction Accuracy')
    plt.xlabel('Model')
    
    # Rotate x-axis labels
    plt.xticks(rotation=45)
    
    # Save the plot to a file
    plt.savefig(filename, format='jpeg')
    plt.close()


create_strip_plot(pred_accs['pri_miRNA'], 'Prediction Accuracies for pri_miRNA', 'pri_miRNA_strip_plot.jpeg')
create_strip_plot(pred_accs['human_mRNA'], 'Prediction Accuracies for human_mRNA', 'human_mRNA_strip_plot.jpeg')
