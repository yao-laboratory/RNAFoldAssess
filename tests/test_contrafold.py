import path

from RNAFoldAssess.models import ContraFold, DataPoint
from RNAFoldAssess.models import DSCI


class TestContraFold:
    # Testing with C009C
    base_data_path = "/common/yesselmanlab/ewhiting/ss_deeplearning_data/data"
    datum = DataPoint.factory(f'{base_data_path}/C009C.json')[0]
    input_file_path = datum.to_seq_file()
    model = ContraFold()
    # Remember, ContraFold is just EternaFold with default parameters
    model_path = path.Path("/home/yesselmanlab/ewhiting/EternaFold").abspath()

    def test_prediction(self):
        self.model.execute(self.model_path, self.input_file_path)
        prediction = self.model.get_ss_prediction()
        scorer = DSCI(self.datum, self.model.get_ss_prediction(), 'ContraFold', evaluate_immediately=True, DMS=True)
        metrics = scorer.metrics
        assert(metrics['accuracy'] > 0.7)
