import pytest

from RNAFoldAssess.models import Scorer, DSCI, DataPoint, BasePairScorer

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


class TestBasePairScorer:
    real = ".(..)..(.(..))."
    predicted = ".(...).(.(..))."

    def test_parse_structure(self):
        parsed = BasePairScorer.parse_structure(self.real)
        expected_positives = [
            (1, 4),
            (7, 13),
            (9, 12)
        ]
        assert(parsed == expected_positives)

    def test_with_no_lenience(self):
        scorer = BasePairScorer(self.real, self.predicted)
        scorer.evaluate()
        expected_report = "Sensitivity: 0.667, PPV: 0.667, F1: 0.667"
        assert(scorer.report() == expected_report)

    def test_report_precision(self):
        scorer = BasePairScorer(self.real, self.predicted)
        scorer.evaluate()
        expected_report = "Sensitivity: 0.66667, PPV: 0.66667, F1: 0.66667"
        assert(scorer.report(precision=5) == expected_report)

    def test_with_1_lenience(self):
        scorer = BasePairScorer(self.real, self.predicted, 1)
        scorer.evaluate()
        expected_report = "Sensitivity: 1.0, PPV: 1.0, F1: 1.0"
        assert(scorer.report() == expected_report)

    def test_false_negative_calculation1(self):
        real = ".(.)..(.)."
        pred = ".(.)......"
        scorer = BasePairScorer(real, pred)
        scorer.evaluate()
        assert(scorer.fn == 1)

    def test_false_negative_calculation2(self):
        real = ".(.)..(.)."
        pred = "(..)..(..)"
        scorer = BasePairScorer(real, pred)
        scorer.evaluate()
        assert(scorer.fn == 2)

    def test_false_negative_calculation3(self):
        real = ".(.)..(.)."
        pred = "(..)..(.).."
        scorer = BasePairScorer(real, pred, 1)
        scorer.evaluate()
        assert(scorer.fn == 0)

    def test_false_negative_calculation4(self):
        real = ".(.)..(.)."
        pred = "(..)......"
        scorer = BasePairScorer(real, pred, 1)
        scorer.evaluate()
        assert(scorer.fn == 1)

    def test_false_negative_calculation6(self):
        real = ".(.)..(.)."
        pred = "(.)..(.).."
        scorer = BasePairScorer(real, pred)
        scorer.evaluate()
        assert(scorer.fn == 2)

    def test_perfect_match(self):
        scorer = BasePairScorer(self.real, self.real)
        scorer.evaluate()
        assert(scorer.sensitivity == 1.0)
        assert(scorer.ppv == 1.0)
        assert(scorer.f1 == 1.0)



