import os
from scipy.stats import mannwhitneyu

from .data_point import *


class DecoratedDataPoint(DataPoint):
    def __init__(self, data_hash, cohort=None):
        super().__init__(data_hash, cohort)
        self.base_data_path = os.path.abspath("./data")
        self.bf_predictions = []
        self.algo_predictions = []

    def algorithmic_prediction_location(self):
        path = f"{self.base_data_path}/rna_structure_predictions/{self.cohort}/{self.name}_ss"
        return path

    def bf_prediction_location(self):
        path = f"{self.base_data_path}/scores/{self.cohort}_scores/{self.name}"
        return path

    def init_algorithmic_predictions(self):
        f = open(self.algorithmic_prediction_location())
        contents = f.read()
        f.close()
        blocks = contents.split(">")
        try:
            blocks.remove("")
        except ValueError:
            pass
        for block in blocks:
            block = block.split("\n")
            try:
             block.remove("")
            except ValueError:
                pass
            structure = block[-1]
            score = self.evaluate(structure)
            self.algo_predictions.append({
                "structure": structure,
                "accuracy": score[0],
                "p": score[1]
            })


    def init_bf_predictions(self):
        f = open(self.bf_prediction_location())
        contents = f.read()
        f.close()
        data_blocks = contents.split("\n\n")
        header = data_blocks.pop(0).split("\n")
        self.molecule_name = header[0].split()[1]
        self.sequence = header[1].split()[1]
        for prediction in data_blocks[:-1]: # To -1 because last item is empty
            prediction = prediction.split("\n")
            self.bf_predictions.append({
                "structure": prediction[0].split()[1],
                "accuracy": float(prediction[1].split()[1]),
                "p": prediction[2].split()[1]
            })


    @staticmethod
    def factory(path, name_prefix):
        f = open(path)
        json_data = json.loads(f.read())
        f.close()
        data_points = []
        for datum in json_data:
            data_points.append(DecoratedDataPoint(datum, name_prefix))
        return data_points

    def evaluate(self, structure):
        if len(self.sequence) != len(structure):
            print("Sequence length and secondary structure length don't match")
            print(f"Sequence length is {len(self.sequence)}, ss length is {len(structure)}")
            return False

        if len(self.reactivities) != len(structure):
            print("Reactivities length and secondary structure length don't match")
            print(f"Reactivities length is {len(self.reactivities)}, ss length is {len(structure)}")
            return False

        paired, unpaired = [], []
        for nt, db, val in zip(self.sequence, structure, self.reactivities):
            if nt != "A" and nt != "C":
                continue
            if db == ".":
                unpaired.append(val)
            else:
                paired.append(val)

        result = mannwhitneyu(unpaired, paired, alternative="greater")
        denominator = len(paired) * len(unpaired)
        return (result.statistic / denominator, result.pvalue)
