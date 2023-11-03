import pytest

from RNAFoldAssess.models import Scorer, DSCI, DSCIException, DataPoint, BasePairScorer

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

    def test_raise_exception(self):
        with pytest.raises(DSCIException) as e_info:
            DSCI(self.datum, ".(.)............", "mock algo", evaluate_immediately=True)
        assert(str(e_info.value) == "Please specify if reactivity data is DMS or SHAPE")

    # DMS based tests
    def test_perfect_prediction(self):
        prediction = ".(.)............"
        scorer = DSCI(self.datum, prediction, "mock algo", evaluate_immediately=True, DMS=True)
        assert(scorer.accuracy == 1.0)
        assert(scorer.p_value < 0.002)
        assert("DataPointMock" in scorer.report())

    def test_bad_prediction(self):
        prediction = "(.).()()()()()()"
        scorer = DSCI(self.datum, prediction, "mock algo", evaluate_immediately=True, DMS=True)
        assert(scorer.accuracy == 0.0)

    def test_manual_entry(self):
        # Want to make sure the static method
        # and instance methodbehave identically
        prediction = ".(.)............"
        scorer = DSCI(self.datum, prediction, "mock algo", evaluate_immediately=True, DMS=True)
        static_scorer = DSCI.score(
            self.datum.sequence,
            prediction,
            self.datum.reactivities,
            DMS=True
        )
        assert(scorer.accuracy == static_scorer["accuracy"])
        assert(scorer.p_value == static_scorer["p"])

    # SHAPE based tests
    def test_paired_unpaired_retriever(self):
        seq = "UUCCAAGCUCUG"
        ss  = "..(...)....."
        reactivities = [
            0.0, 0.0, 0.9,
            0.0, 0.0, 0.0,
            0.9, 0.0, 0.0,
            0.0, 0.0, 0.0
        ]
        DMS_expected_paired = [0.9]
        DMS_expected_unpaired = [0.0, 0.0, 0.0, 0.0, 0.0]
        SHAPE_expected_paired = [0.9, 0.9]
        SHAPE_expected_unpaired = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

        d_p, d_up = DSCI.get_paired_and_unpaired_nucleotides(seq, ss, reactivities, "DMS")
        assert(d_p == DMS_expected_paired)
        assert(d_up == DMS_expected_unpaired)

        s_p, s_up = DSCI.get_paired_and_unpaired_nucleotides(seq, ss, reactivities, "SHAPE")
        assert(s_p == SHAPE_expected_paired)
        assert(s_up == SHAPE_expected_unpaired)

    def test_perfect_prediction_SHAPE(self):
        prediction = ".(.)............"
        scorer = DSCI(self.datum, prediction, "mock algo", evaluate_immediately=True, SHAPE=True)
        assert(scorer.accuracy == 1.0)
        assert(scorer.p_value < 0.002)
        assert("DataPointMock" in scorer.report())

    def test_bad_prediction_SHAPE(self):
        prediction = "(.).()()()()()()"
        scorer = DSCI(self.datum, prediction, "mock algo", evaluate_immediately=True, SHAPE=True)
        assert(scorer.accuracy == 0.0)

    def test_manual_entry_SHAPE(self):
        # Want to make sure the static method
        # and instance methodbehave identically
        prediction = ".(.)............"
        scorer = DSCI(self.datum, prediction, "mock algo", evaluate_immediately=True, SHAPE=True)
        static_scorer = DSCI.score(
            self.datum.sequence,
            prediction,
            self.datum.reactivities,
            SHAPE=True
        )
        assert(scorer.accuracy == static_scorer["accuracy"])
        assert(scorer.p_value == static_scorer["p"])


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

    def test_acceptable_locations1(self):
        structure = ".(.)..(..(.)..).."
        scorer = BasePairScorer(structure, structure)
        expected_locations = [
            (1, 3),
            (6, 14),
            (9, 11)
        ]
        assert(scorer.acceptable_locations == expected_locations)

    def test_acceptable_locations2(self):
        structure = ".(.)..(..(.)..).."
        scorer = BasePairScorer(structure, structure, bp_lenience=1)
        expected_locations = [
            (1, 3), # Actual location
            (0, 3),
            (1, 2),
            (2, 3),
            (1, 4),

            (6, 14), # Actual location
            (5, 14),
            (6, 13),
            (7, 14),
            (6, 15),

            (9, 11), # Actual location
            (8, 11),
            (9, 10),
            (10, 11),
            (9, 12)
        ]
        for loc in scorer.acceptable_locations:
            assert(loc in expected_locations)

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



