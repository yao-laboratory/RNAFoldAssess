import os, statistics

import seaborn as sns
import matplotlib.pyplot as plt


class Predictions:
    def __init__(self, dataset_name, ds_name_index, dp_name_index, seq_index, pred_index, acc_index, pred_file, go_immediately=True):
        self.dataset_name = dataset_name
        self.ds_name_index = ds_name_index
        self.dp_name_index = dp_name_index
        self.seq_index = seq_index
        self.pred_index = pred_index
        self.acc_index = acc_index
        self.pred_file = pred_file
        self.data = None
        self.accs = None
        self.easy_data_points = []
        self.hard_data_points = []
        self.other_data_points = []
        self.q1 = None
        self.q2 = None
        self.q3 = None
        self.q4 = None
        if go_immediately:
            self.calculate_stats()
            self.separate_predictions()
            self.create_separated_pred_files(self.dataset_name)
            self.create_figures()


    def calculate_stats(self):
        with open(self.pred_file) as fh:
            data = fh.readlines()

        if data[0].startswith("algo"):
            data.pop(0)

        print("Assembling data")
        self.data = [d.split(", ") for d in data]
        if self.dataset_name.startswith("RNAndria"):
            # pri_miRNA is hash, human_mRNA is hsa-mir
            if "mRNA" in self.dataset_name:
                self.data = [d for d in self.data if  d[self.ds_name_index] == "RNAndria" and "hsa-mir" in d[self.dp_name_index]]
            else:
                self.data = [d for d in self.data if d[self.ds_name_index] == "RNAndria" and "hsa-mir" not in d[self.dp_name_index]]
        else:
            self.data = [d for d in self.data if d[self.ds_name_index] == self.dataset_name]
        self.accs = [float(d[self.acc_index].strip()) for d in self.data]

        self.q2 = statistics.median(self.accs)
        # Split accuracies into two halves
        lower_half = self.accs[:len(self.accs)//2]
        upper_half = self.accs[(len(self.accs)+1)//2:]  # Adjust for odd-sized lists
        self.q1 = statistics.median(lower_half)
        self.q3 = statistics.median(upper_half)


    def separate_predictions(self):
        print("Separating predictions")
        if not self.data:
            raise Exception("You need to run `calculate_stats` first")

        for d in self.data:
            acc = float(d[self.acc_index])
            if acc <= self.q1:
                self.hard_data_points.append(d)
            elif acc >= self.q3:
                self.easy_data_points.append(d)
            else:
                self.other_data_points.append(d)

    
    def create_separated_pred_files(self, fname_prefix):
        if self.easy_data_points == []:
            raise Exception("You need to run `separate_predictions` first")

        with open(f"{fname_prefix}_easy.txt", "w") as fh:
            for edp in self.easy_data_points:
                fh.write("".join(edp))

        with open(f"{fname_prefix}_hard.txt", "w") as fh:
            for hdp in self.hard_data_points:
                fh.write("".join(hdp))

        with open(f"{fname_prefix}_other.txt", "w") as fh:
            for odp in self.other_data_points:
                fh.write("".join(odp))


    def create_figures(self):
        print("Creating figures")
        if self.easy_data_points == []:
            raise Exception("Yoou need to run `separate_predictions` first")

        # Get data for easy datapoints
        easy_lens = []
        easy_gc = []
        easy_bp_rate = []
        for d in self.easy_data_points:
            seq = d[self.seq_index]
            seq_length = len(seq)
            easy_lens.append(seq_length)
            seq_gc = Predictions.get_gc_content(seq)
            easy_gc.append(seq_gc)
            stc = d[self.pred_index]
            bp_rate = Predictions.get_bp_rate(stc)
            easy_bp_rate.append(bp_rate)

        # Get data for hard data points
        hard_lens = []
        hard_gc = []
        hard_bp_rate = []
        for d in self.hard_data_points:
            seq = d[self.seq_index]
            seq_length = len(seq)
            hard_lens.append(seq_length)
            seq_gc = Predictions.get_gc_content(seq)
            hard_gc.append(seq_gc)
            stc = d[self.pred_index]
            bp_rate = Predictions.get_bp_rate(stc)
            hard_bp_rate.append(bp_rate)

        # Call method to make plots
        Predictions.make_plot(
            easy_lens,
            hard_lens,
            f"Length Dist. in {self.dataset_name} predictions",
            f"{self.dataset_name}_len_density_plot.jpg"
        )
        Predictions.make_plot(
            easy_gc,
            hard_gc,
            f"GC-Content Dist. in {self.dataset_name} predictions",
            f"{self.dataset_name}_gc_density_plot.jpg"
        )
        Predictions.make_plot(
            easy_bp_rate,
            hard_bp_rate,
            f"BP rate Dist. in {self.dataset_name} predictions",
            f"{self.dataset_name}_bp_density_plot.jpg"
        )
        print("Completed figures")


    @staticmethod
    def make_plot(easy_data, hard_data, title, file_name):
        print(f"Making {title}")

        sns.kdeplot(easy_data, label="Easy Datapoints", color="blue", gridsize=400)
        sns.kdeplot(hard_data, label="Hard Datapoints", color="orange", gridsize=400)

        plt.title(title)
        plt.legend()  # Explicitly adds the legend
        plt.savefig(fname=file_name, format="jpg")
        plt.clf()


    @staticmethod
    def get_gc_content(seq):
        g_content = seq.count("g") + seq.count("G")
        c_content = seq.count("c") + seq.count("C")
        gc_content = g_content + c_content
        return gc_content / len(seq)

    @staticmethod
    def get_bp_rate(structure):
        bp_count = structure.count("(") * 2
        if bp_count == 0:
            return 0.0
        else:
            return len(structure) / bp_count



file_path = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions/chemical_mapping_matched_set.txt"
# eterna_preds = Predictions("EternaData", 0, 2, 3, 4, 5, file_path)
# ydata_preds = Predictions("YesselmanLab", 0, 2, 3, 4, 5, file_path)
# ribo_preds = Predictions("Ribonanza", 0, 2, 3, 4, 5, file_path)
rnandria_preds = Predictions("RNAndria_human_mRNA", 0, 2, 3, 4, 5, file_path)
rnandria_preds = Predictions("RNAndria_pri_miRNA", 0, 2, 3, 4, 5, file_path)

# Make fasta files
dirs = ["EternaData", "YesselmanLab", "Ribonanza", "RNAndria"]

