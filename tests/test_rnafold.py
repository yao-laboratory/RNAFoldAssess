import os

from RNAFoldAssess.models import RNAFold, DataPoint
from RNAFoldAssess.models import DSCI


class TestRNAFold:
    # Testing with C009C
    base_data_path = "/common/yesselmanlab/ewhiting/ss_deeplearning_data/data"
    datum = DataPoint.factory(f'{base_data_path}/C009C.json')[0]
    model = RNAFold()
    model_path = os.path.abspath("/home/yesselmanlab/ewhiting/ViennaRNA/bin/RNAfold")

    def test_prediction(self):
        input_file_path = self.datum.to_fasta_file()
        self.model.execute(self.model_path, input_file_path, remove_file_when_done=True)
        prediction = self.model.get_ss_prediction()
        scorer = DSCI(self.datum, prediction, 'RNAFold', evaluate_immediately=True, DMS=True)
        metrics = scorer.metrics
        assert(metrics['accuracy'] > 0.7)
