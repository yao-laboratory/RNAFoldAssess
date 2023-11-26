from .scorer import Scorer


class BasePairScorer(Scorer):
    def __init__(self, true_structure, predicted_structure, bp_lenience=0):
        self.true_structure = true_structure
        self.predicted_structure = predicted_structure
        self.bp_lenience = bp_lenience
        self.true_structure = BasePairScorer.parse_structure(self.true_structure)
        self.predicted_structure = BasePairScorer.parse_structure(self.predicted_structure)
        self.acceptable_locations = []
        self.tp = 0
        self.fp = 0
        self.fn = 0
        self.get_acceptable_locations()
        self.get_false_negatives()
        self.get_tp_and_fp()

    def evaluate(self):
        if (self.tp + self.fn) == 0:
            self.sensitivity = 0.0
        else:
            self.sensitivity = self.tp / (self.tp + self.fn)

        if (self.tp + self.fp) == 0:
            self.ppv = 0
        else:
            self.ppv = self.tp / (self.tp + self.fp)

        if (self.sensitivity + self.ppv) == 0:
            self.f1 = 0
        else:
            self.f1 = (2 * self.sensitivity * self.ppv) / (self.sensitivity + self.ppv)

    def get_tp_and_fp(self):
        for pred_bp in self.predicted_structure:
            if pred_bp in self.acceptable_locations:
                self.tp += 1
            else:
                self.fp += 1

    def get_false_negatives(self):
        fn = 0
        if len(self.true_structure) > 0 and len(self.predicted_structure) == 0:
            self.fn += len(self.true_structure)
        else:
            for bp in self.true_structure:
                pos_locs = [bp]
                i, j = bp
                for r in range(self.bp_lenience):
                    e = r + 1
                    pos_locs.append((i + e, j))
                    pos_locs.append((i, j + e))
                    pos_locs.append((i - e, j))
                    pos_locs.append((i, j - e))

                for pbp in self.predicted_structure:
                    if pbp in pos_locs:
                        fn = 0
                        break
                    else:
                        fn = 1
                self.fn += fn

    def get_acceptable_locations(self):
        """
        Get all acceptable locations given the provided leniency. In other
        words, if lenience of 1, add one of the true locations is (2, 4),
        we need to add (3, 4), (2, 5), (1, 4), and (1, 3) to the list of
        acceptable locations. With this list, we can check each predicted
        location against the acceptable location and successfully record
        either a true positive or false positive.
        """
        for true_bp in self.true_structure:
            self.acceptable_locations.append(true_bp) # (i, j)
            real_start, real_end = true_bp
            for i in range(self.bp_lenience):
                lenience = i + 1
                self.acceptable_locations.append((real_start + lenience, real_end)) # (i + e, j)
                self.acceptable_locations.append((real_start, real_end + lenience)) # (i, j + e)
                self.acceptable_locations.append((real_start - lenience, real_end)) # (i - e, j)
                self.acceptable_locations.append((real_start, real_end - lenience)) # (i, j - e)

    def report(self, precision=3):
        report = f"Sensitivity: {round(self.sensitivity, precision)}, "
        report += f"PPV: {round(self.ppv, precision)}, "
        report += f"F1: {round(self.f1, precision)}"
        return report

    @staticmethod
    def parse_structure(structure):
        # structure exampe: "..((((...))))..((..))."
        bps = []
        for i1, c1 in enumerate(structure):
            if c1 != '(':
                continue
            count = 1
            for i2, c2 in enumerate(structure[i1 + 1:]):
                if c2 == '(':
                    count += 1
                elif c2 == ')':
                    count -= 1
                    if count == 0:
                        bps.append((i1, i1 + i2 + 1))
                        break
        return bps
