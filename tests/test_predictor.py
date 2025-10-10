import pytest
from unittest.mock import MagicMock

from RNAFoldAssess.models import Predictor, DataPoint


class TestPredictor:
    model = Predictor()

    def test_output_is_empty_string(self):
        assert(self.model.output == "")

    def test_execute_not_implemented(self):
        dp_mock = MagicMock(DataPoint)
        with pytest.raises(NotImplementedError):
            self.model.execute(dp_mock)

    def test_get_ss_prediction_not_implemented(self):
        with pytest.raises(NotImplementedError):
            self.model.get_ss_prediction()

    def test_get_mfe_not_implemented(self):
        with pytest.raises(NotImplementedError):
            self.model.get_mfe()
