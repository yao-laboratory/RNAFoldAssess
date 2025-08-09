from scipy.stats import mannwhitneyu

from .scorer import Scorer


class DSCI(Scorer):
    """
    This class implements the DSCI scoring methd, which makes use of the
    Mann-Whitney U-Test. Note that there are two options to run this scoring
    mechanism: with a static method (score) or an instance method (evaluate).

    The static method, `score`, requires as input a nucleotide sequence, a
    predicted secondary structure, chemical mapping reactivity data, and an
    indication of whether the chemical mapping reactivity data comse from a
    DMS or SHAPE experiment. Note that the implementation of DSCI differs
    depending on the type of chemical mapping data given.

    The following code provides an example usage of the DSCI class:

    ```python
    from RNAFoldAssess.models.scorers import DSCI

    squence = "ACUGACUGAAAAAAAA"
    predicted_structure = ".(.)............"
    dms_reactivities = [
        10.0, 0.0, 10.0, 0.0,
        10.0, 10.0, 10.0, 10.0,
        10.0, 10.0, 10.0, 10.0,
        10.0, 10.0, 10.0, 10.0
    ]

    score = DSCI.score(
        sequence,
        predicted_structure,
        dms_reactivities,
        DMS=True
    )
    ```

    The `score` method returns a dictionary with an "accuracy" and "p" keys.
    The "accuracy" key contains a number between 0 and 1 and is the output
    of the Mann-Whitney U-Test, the "p" is the P-value from the test. In
    the above example, the value of `score` would be very similar to:

        {
            "accuracy": 1.0,
            "p": 0.002
        }

    Using the instance method, `evaluate`, works similarly. First, you have
    to create a DSCI object with a `data_point` attribute. Note that the
    `data_point` has to be an object with `name`, `sequence`, and `reactivites`
    attributes. There is a `DataPoint` class in this package that can be
    used, but as long as the object has those attributes, it can be used
    as the DSCI object's `data_point` attribute.

    The following code provides an example usage of the `evaluate` method:

    ```python
    from RNAFoldAssess.models.scorers import DSCI
    from RNAFoldAssess.models import DataPoint
    data_point = DataPoint(
        {
            "name": "DataPointMock",
            "sequence": "ACUGACUGAAAAAAAA",
            # Points 1 and 3
            "data": [
                10.0, 0.0, 10.0, 0.0,
                10.0, 10.0, 10.0, 10.0,
                10.0, 10.0, 10.0, 10.0,
                10.0, 10.0, 10.0, 10.0
            ],
            "reads": 1
        }
    )

    scorer = DSCI(self.datum, prediction, "mock algo", DMS=True)
    scorer.evaluate()
    accuracy = scorer.accuracy
    p_value = scorer.p_value
    ```

    Note that running `evaluate` does not return anything, it only sets the
    object's `accuracy` and `p_value` attributes. In order to get either of
    those values, you have to call the `accuracy` or `p_value` attribute.
    In the above example, the `accuracy` value should be close to 1.0 and the
    `p_value` value should be less than 0.02
    """
    def __init__(self,
                 data_point,
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
        reactivity_map = self.data_point.reactivity_map
        testable_reactivities = []
        testable_seq = ""
        testable_dbn = ""
        for pos, reactivity in reactivity_map.items():
            testable_reactivities.append(reactivity)
            testable_seq += self.data_point.sequence[pos]
            testable_dbn += self.secondary_structure[pos]
        score = DSCI.score(
            testable_seq,
            testable_dbn,
            testable_reactivities,
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
