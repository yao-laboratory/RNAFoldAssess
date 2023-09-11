import path, os

from RNAFoldAssess.models import ContextFold, DataPoint
from RNAFoldAssess.models import DSCI


class TestContextFold:
    # Testing with C009C
    base_data_path = "/common/yesselmanlab/ewhiting/ss_deeplearning_data/data"
    datum = DataPoint.factory(f'{base_data_path}/C009C.json')[0]
    input_file_path = datum.sequence # Not actually a file but keeping it for consistency
    model = ContextFold()
    model_path = path.Path("/home/yesselmanlab/ewhiting/ContextFold_1_00").abspath()

    def test_prediction(self):
        self.model.execute(self.model_path, self.input_file_path)
        prediction = self.model.get_ss_prediction()
        scorer = DSCI(self.datum, self.model.get_ss_prediction(), 'Context Fold')
        metrics = scorer.metrics
        assert(metrics['accuracy'] > 0.7)
