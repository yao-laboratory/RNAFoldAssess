import path, os

from RNAFoldAssess.models import RandomPredictor, DataPoint

class TestRandomPredictor:
    # Testing with C009C
    base_data_path = "/common/yesselmanlab/ewhiting/ss_deeplearning_data/data"
    datum = DataPoint.factory(f'{base_data_path}/C009C.json')[0]
    input_file_path = datum.to_fasta_file()
    model = RandomPredictor()

    def test_prediction(self):
        self.model.execute(fasta_file=self.input_file_path)
        os.remove(self.input_file_path)
        prediction = self.model.get_ss_prediction()
        assert(len(prediction) == len(self.datum.sequence))
