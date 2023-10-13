from scipy.stats import mannwhitneyu

from .scorer import Scorer


# This scorer is called the DSCI method and uses the Man-Whitney U-Test

class DSCI(Scorer):
    def evaluate(self):
        if len(self.data_point.sequence) != len(self.secondary_structure):
            print("Sequence length and secondary structure length don't match")
            return False

        if len(self.data_point.reactivities) != len(self.secondary_structure):
            print("Reactivities length and secondary structure length don't match")
            return False

        paired, unpaired = [], []
        for nt, db, val in zip(self.data_point.sequence, self.secondary_structure, self.data_point.reactivities):
            if nt != "A" and nt != "C":
                continue
            if db == ".":
                unpaired.append(val)
            else:
                paired.append(val)

        result = mannwhitneyu(unpaired, paired, alternative="greater")
        denominator = len(paired) * len(unpaired)
        metrics = (result.statistic / denominator, result.pvalue)
        self.accuracy = metrics[0]
        self.p_value = metrics[1]
        self.metrics = {
            "data_point_name": self.data_point.name,
            "accuracy": self.accuracy,
            "p": self.p_value,
            "algorithm": self.algorithm
        }

    def report(self):
        return f"{self.data_point.name}, {self.accuracy}, {self.p_value}"
