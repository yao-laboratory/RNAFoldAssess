import os

from RNAFoldAssess.models import RNAFold, DataPoint
from RNAFoldAssess.models import DSCI


class TestRNAFold:
    # Testing with C009C
    base_data_path = "./tests/fixtures"
    datum = DataPoint.factory(f'{base_data_path}/C009C.json')[0]
    model = RNAFold()
    model_path = os.path.abspath("/home/runner/work/RNAFoldAssess/RNAFoldAssess/RNAFoldAssess/ViennaRNA-2.6.4/bin/RNAfold")
    def test_prediction(self):
        input_file_path = self.datum.to_fasta_file()
        self.model.execute(self.model_path, input_file_path, remove_file_when_done=True)
        prediction = self.model.get_ss_prediction()
        scorer = DSCI(self.datum, prediction, 'RNAFold', evaluate_immediately=True, DMS=True)
        metrics = scorer.metrics
        assert(metrics['accuracy'] > 0.7)
