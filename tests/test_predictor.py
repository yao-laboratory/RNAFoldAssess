import pytest

from RNAFoldAssess.models import Predictor


class TestPredictor:
    model = Predictor()

    def test_output_is_empty_string(self):
        assert(self.model.output == "")
    
    def test_execute_not_implemented(self):
        with pytest.raises(NotImplementedError):
            self.model.execute()
    
    def test_get_ss_prediction_not_implemented(self):
        with pytest.raises(NotImplementedError):
            self.model.get_ss_prediction()
    
    def test_get_mfe_not_implemented(self):
        with pytest.raises(NotImplementedError):
            self.model.get_mfe()
