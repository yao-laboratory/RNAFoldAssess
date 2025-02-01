import os

import pytest

from RNAFoldAssess.models import RNAFold, DataPoint
from RNAFoldAssess.models import DSCI

# @pytest.mark.skip(reason="Still figuring out how to make this work in CI")
class TestRNAFold:
    # Testing with C009C
    base_data_path = "./tests/fixtures"
    datum = DataPoint.factory(f'{base_data_path}/C009C.json')[0]
    model = RNAFold()
    def test_prediction_with_fasta_file(self):
        input_file_path = self.datum.to_fasta_file()
        self.model.execute(input_file_path, source_type="fasta")
        prediction = self.model.get_ss_prediction()
        scorer = DSCI(self.datum, prediction, 'RNAFold', evaluate_immediately=True, DMS=True)
        metrics = scorer.metrics
        assert(metrics['accuracy'] > 0.7)

    def test_prediction_with_string_input(self):
        base_data_path = "./tests/fixtures"
        datum = DataPoint.factory(f'{base_data_path}/C009C.json')[0]
        sequence = datum.sequence
        self.model.execute(sequence)
        prediction = self.model.get_ss_prediction()
        scorer = DSCI(self.datum, prediction, 'RNAFold', evaluate_immediately=True, DMS=True)
        metrics = scorer.metrics
        assert(metrics['accuracy'] > 0.7)
