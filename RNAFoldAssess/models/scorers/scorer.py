# This is the base model for scoring methods. All scoring methods
# need to inherit this class and override the `evaluate` method.


class Scorer:
    def __init__(self, data_point, secondary_structure, algorithm, evaluate_immediately=True):
        self.data_point = data_point
        self.secondary_structure = secondary_structure
        self.algorithm = algorithm
        self.metrics = {}
        if evaluate_immediately:
            self.evaluate()

    def evaluate(self):
        raise NotImplementedError("The `evaluate` method was not created for this scorer")
