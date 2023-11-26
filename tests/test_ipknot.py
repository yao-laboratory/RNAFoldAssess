import path, os

from RNAFoldAssess.models import IPknot, DataPoint
from RNAFoldAssess.models import DSCI


class TestIPknot:
    # Testing with C009C
    base_data_path = "/common/yesselmanlab/ewhiting/ss_deeplearning_data/data"
    datum = DataPoint.factory(f'{base_data_path}/C009C.json')[0]
    input_file_path = datum.to_fasta_file()
    model = IPknot()
    model_path = path.Path("/common/yesselmanlab/ewhiting/ipknot-1.1.0-x86_64-linux/ipknot").abspath()

    def test_prediction(self):
        self.model.execute(self.model_path, self.input_file_path, remove_file_when_done=False)
        prediction = self.model.get_ss_prediction()
        scorer = DSCI(self.datum, self.model.get_ss_prediction(), 'IPknot', evaluate_immediately=True, DMS=True)
        metrics = scorer.metrics
        assert(metrics['accuracy'] > 0.7)

    def test_non_pseudoknot_prediction(self):
        self.model.execute(self.model_path, self.input_file_path)
        prediction = self.model.get_ss_prediction_ignore_pseudoknots()
        scorer = DSCI(self.datum, self.model.get_ss_prediction(), 'IPknot', evaluate_immediately=True, DMS=True)
        metrics = scorer.metrics
        assert(metrics['accuracy'] > 0.7)
