from scipy.stats import mannwhitneyu


class Evaluator:
    def __init__(self, data_point, secondary_structure, algorithm, evaluate_immediately=True):
        self.data_point = data_point
        self.secondary_structure = secondary_structure
        self.algorithm = algorithm
        if evaluate_immediately:
            self.evaluate()

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
