class Scorer:
    """
    This is the base model for scoring methods. All scoring methods
    need to inherit this class and override the `evaluate` method.
    """
    def __init__(self, *args, **kwargs):
        pass

    def evaluate(self):
        """
        Override this method to apply the scoring technique you are writing.
        Note: the `data_point` member of this class *should* be configured
        to have the data you need to run the scoring algorithm. For example,
        an implementation of the DSCI scoring algorithm requires a data_point
        object with sequence data, DMS or SHAPE data, and a predicted
        secondary structure in dot-bracket notation. Make sure the inputs to
        your scoring algorithm have the data necessary!
        """
        raise NotImplementedError("The `evaluate` method was not created for this scorer")

    def report(self):
        """
        Override this method in your scorers to output a string
        reporting the score of the evaluation. This method is
        intended for writing or printing score information on a
        per-prediction basis.
        """
        raise NotImplementedError("The `report` method was not created for this scorer")
