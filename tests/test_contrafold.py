import os

from RNAFoldAssess.models import ContraFold, DataPoint
from RNAFoldAssess.models import DSCI


class TestContraFold:
    # Testing with C009C
    base_data_path = "./tests/fixtures"
    datum = DataPoint.factory(f'{base_data_path}/C009C.json')[0]
    input_file_path = datum.to_seq_file()
    model = ContraFold()
    # Remember, ContraFold is just EternaFold with default parameters
    model_path = os.path.abspath("/home/runner/work/RNAFoldAssess/EternaFold")

    def test_prediction(self):
        self.model.execute(self.model_path, self.input_file_path)
        prediction = self.model.get_ss_prediction()
        scorer = DSCI(self.datum, prediction, 'ContraFold', evaluate_immediately=True, DMS=True)
        metrics = scorer.metrics
        assert(metrics['accuracy'] > 0.7)
