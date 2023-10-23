from scipy.stats import mannwhitneyu

from .scorer import Scorer


# This scorer is called the DSCI method and uses the Man-Whitney U-Test

class DSCI(Scorer):
    @staticmethod
    def score(sequence, secondary_structure, reactivities):
        if len(sequence) != len(secondary_structure):
            print("Sequence length and secondary structure length don't match")
            return False

        if len(reactivities) != len(secondary_structure):
            print("Reactivities length and secondary structure length don't match")
            return False

        paired, unpaired = [], []
        for nt, db, val in zip(sequence, secondary_structure, reactivities):
            if nt != "A" and nt != "C":
                continue
            if db == ".":
                unpaired.append(val)
            else:
                paired.append(val)

        result = mannwhitneyu(unpaired, paired, alternative="greater")
        denominator = len(paired) * len(unpaired)
        metrics = (result.statistic / denominator, result.pvalue)
        return {
            "accuracy": metrics[0],
            "p": metrics[1]
        }

    def evaluate(self, precision=4):
        score = DSCI.score(
            self.data_point.sequence,
            self.secondary_structure,
            self.data_point.reactivities
        )
        self.accuracy = score["accuracy"]
        self.p_value = score["p"]
        self.metrics = {
            "data_point_name": self.data_point.name,
            "accuracy": round(self.accuracy, precision),
            "p": round(self.p_value, precision),
            "algorithm": self.algorithm
        }

    def eval_manual_entry(self, predicted_structure, sequence, reactivities):
        pass

    def report(self):
        return f"{self.data_point.name}, {self.accuracy}, {self.p_value}"
