import os

from RNAFoldAssess.models import RNAStructure, DataPoint
from RNAFoldAssess.models import DSCI


class TestRNAStructure:
    # Testing with C009C
    base_data_path = "/common/yesselmanlab/ewhiting/ss_deeplearning_data/data"
    datum = DataPoint.factory(f'{base_data_path}/C009C.json')[0]
    model = RNAStructure()
    model_path = "/util/opt/anaconda/deployed-conda-envs/packages/rnastructure/envs/rnastructure-6.1/bin/Fold"
    # HCC Swan housekeeping:
    os.system("module load rnastructure")
    os.system("export DATAPATH=/util/opt/anaconda/deployed-conda-envs/packages/rnastructure/envs/rnastructure-6.1/share/rnastructure/data_tables")

    def test_prediction(self):
        input_file_path = self.datum.to_fasta_file()
        self.model.execute(self.model_path, input_file_path, "some_output.ct")
        prediction = self.model.get_ss_prediction()
        scorer = DSCI(self.datum, self.model.get_ss_prediction(), 'RNAStructure', evaluate_immediately=True, DMS=True)
        metrics = scorer.metrics
        assert(metrics['accuracy'] > 0.7)
        # clean up
        os.remove("seq_5865.fasta")
        os.remove(self.model.path_to_ct_file)
