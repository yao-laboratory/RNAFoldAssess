from scipy.stats import mannwhitneyu

from RNAFoldAssess.models.scorers.DSCI import DSCIException

from .scorer import Scorer


class EternaScorer(Scorer):
    def __init__(self,
                 data_point=None,
                 secondary_structure=None,
                 algorithm=None,
                 evaluate_immediately=False,
                 DMS=False,
                 SHAPE=False,
                 CMCT=False):
        self.data_point = data_point
        self.secondary_structure = secondary_structure
        self.algorithm = algorithm
        self.DMS = DMS
        self.SHAPE = SHAPE
        self.metrics = {}
        if evaluate_immediately:
            self.evaluate()

    @staticmethod
    def score(sequence, secondary_structure, reactivities, unpaired_threshold=0.5, paired_threshold=0.25, DMS=False, SHAPE=False, CMCT=False, experiment_type=""):
        reactivity_types = [DMS, SHAPE, CMCT]
        if reactivity_types.count(True) != 1 and experiment_type not in ["DMS", "SHAPE", "CMCT"]:
            raise DSCIException("Please specify if reactivity data is DMS, SHAPE, or CMCT")

        if len(sequence) != len(secondary_structure):
            raise DSCIException(f"Sequence length ({len(sequence)}) and secondary structure length ({len(secondary_structure)}) don't match.")

        if len(reactivities) != len(secondary_structure):
            raise DSCIException(f"Reactivities length ({len(reactivities)}) and secondary structure length ({len(secondary_structure)}) don't match.")

        if DMS:
            experiment_type = "DMS"
        elif SHAPE:
            experiment_type = "SHAPE"
        elif CMCT:
            experiment_type = "CMCT"

        score = 0
        scored_length = 0
        for i, nt in enumerate(sequence):
            if experiment_type == "CMCT" and (nt != "G" and nt != "U"):
                continue
            if experiment_type == "DMS" and (nt != "A" and nt != "C"):
                continue

            stc = secondary_structure[i]
            reactivity = reactivities[i]
            scored_length += 1
            if stc in ".[]}{" and reactivity >= unpaired_threshold:
                score += 1
            if stc in "()" and reactivity <= paired_threshold:
                score += 1

        return score / scored_length



