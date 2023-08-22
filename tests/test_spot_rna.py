import path, os

from RNAFoldAssess.models import SPOT_RNA, DataPoint, Evaluator


class TestSPOT_RNA:
    # Testing with C009C
    base_data_path = "/common/yesselmanlab/ewhiting/ss_deeplearning_data/data"
    datum = DataPoint.factory(f'{base_data_path}/C009C.json')[0]
    input_file_path = datum.to_fasta_file()
    model = SPOT_RNA()
    model_path = path.Path("/home/yesselmanlab/ewhiting/SPOT-RNA").abspath()

    def test_prediction(self):
        self.model.execute(self.model_path, self.input_file_path)
        prediction = self.model.get_ss_prediction()
        evaluation = Evaluator(self.datum, self.model.get_ss_prediction(), 'SPOT-RNA')
        metrics = evaluation.metrics
        assert(metrics['accuracy'] > 0.5) # This one's not super accurate

