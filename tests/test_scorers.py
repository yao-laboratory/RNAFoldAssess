import pytest

from RNAFoldAssess.models import Scorer, DSCI, DataPoint

class TestBaseClass:
    scorer = Scorer(
        "data_point_mock",
        ".((..))..(...)..",
        "fake_algorithm",
        evaluate_immediately=False
    )

    def test_evaluate_exception(self):
        with pytest.raises(NotImplementedError) as e:
            self.scorer.evaluate()
        assert(str(e) == "<ExceptionInfo NotImplementedError('The `evaluate` method was not created for this scorer') tblen=2>")

    def test_report_exception(self):
        with pytest.raises(NotImplementedError) as e:
            self.scorer.report()
        assert(str(e) == "<ExceptionInfo NotImplementedError('The `report` method was not created for this scorer') tblen=2>")


class TestDSCI:
    # Testing with C009C
    base_data_path = "/common/yesselmanlab/ewhiting/ss_deeplearning_data/data"
    datum = DataPoint(
        {
            "name": "DataPointMock",
            "sequence": "ACUGACUGAAAAAAAA",
            # Points 1 and 3
            "data": [
                10.0, 0.0, 10.0, 0.0,
                10.0, 10.0, 10.0, 10.0,
                10.0, 10.0, 10.0, 10.0,
                10.0, 10.0, 10.0, 10.0
            ],
            "reads": 1
        }
    )

    def test_perfect_prediction(self):
        prediction = ".(.)............"
        scorer = DSCI(self.datum, prediction, "mock algo")
        assert(scorer.accuracy == 1.0)
        assert(scorer.p_value < 0.002)
        assert("DataPointMock" in scorer.report())

    def test_bad_prediction(self):
        prediction = "(.).()()()()()()"
        scorer = DSCI(self.datum, prediction, "mock algo")
        assert(scorer.accuracy == 0.0)
