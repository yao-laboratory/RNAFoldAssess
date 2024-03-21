from scipy.stats import mannwhitneyu

from .scorer import Scorer


# This scorer is called the DSCI method and uses the Mann-Whitney U-Test

class DSCI(Scorer):
    def __init__(self,
                 data_point=None,
                 secondary_structure=None,
                 algorithm=None,
                 evaluate_immediately=False,
                 DMS=False,
                 SHAPE=False):
        self.data_point = data_point
        self.secondary_structure = secondary_structure
        self.algorithm = algorithm
        self.DMS = DMS
        self.SHAPE = SHAPE
        self.metrics = {}
        if evaluate_immediately:
            self.evaluate()

    @staticmethod
    def score(sequence, secondary_structure, reactivities, DMS=False, SHAPE=False):
        if not DMS != SHAPE:
            raise DSCIException("Please specify if reactivity data is DMS or SHAPE")

        if len(sequence) != len(secondary_structure):
            raise DSCIException(f"Sequence length ({len(sequence)}) and secondary structure length ({len(secondary_structure)}) don't match.")

        if len(reactivities) != len(secondary_structure):
            raise DSCIException(f"Reactivities length ({len(reactivities)}) and secondary structure length ({len(secondary_structure)}) don't match.")

        experiment_type = "DMS" if DMS else "SHAPE"
        paired, unpaired = DSCI.get_paired_and_unpaired_nucleotides(
            sequence,
            secondary_structure,
            reactivities,
            experiment_type
        )

        try:
            if not paired:
                paired = [0]
            if not unpaired:
                unpaired = [1.0]
            result = mannwhitneyu(unpaired, paired, alternative="greater")
            denominator = len(paired) * len(unpaired)
            metrics = (result.statistic / denominator, result.pvalue)
            return {
                "accuracy": metrics[0],
                "p": metrics[1]
            }
        except TypeError as e:
            raise DSCITypeError(f"TypeError failure reading sequence {sequence}: {str(e)}")
        except ValueError as e:
            raise DSCIValueError(f"ValueError failure reading sequence {sequence}: {str(e)}")

    @staticmethod
    def get_paired_and_unpaired_nucleotides(sequence, secondary_structure, reactivities, experiment_type):
        if experiment_type not in ["DMS", "SHAPE"]:
            raise DSCIException("Please specify if reactivity data is DMS or SHAPE")

        paired, unpaired = [], []
        for nt, db, val in zip(sequence, secondary_structure, reactivities):
            if experiment_type == "DMS" and (nt != "A" and nt != "C"):
                continue
            if db == ".":
                unpaired.append(val)
            else:
                paired.append(val)

        return paired, unpaired


    def evaluate(self, precision=4):
        score = DSCI.score(
            self.data_point.sequence,
            self.secondary_structure,
            self.data_point.reactivities,
            self.DMS,
            self.SHAPE
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


class DSCIException(Exception):
    pass

class DSCITypeError(Exception):
    pass

class DSCIValueError(Exception):
    pass
