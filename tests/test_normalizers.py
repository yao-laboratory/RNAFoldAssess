from RNAFoldAssess.utils import Normalizers


class TestNormalizationMethods:
    def test_simple_normalizer(self):
        reactivities = [1, 2, 3, 4, 5]
        expected_reactivities = [1/5, 2/5, 3/5, 4/5, 5/5]
        assert(
            Normalizers.simple_normalizer(reactivities) == expected_reactivities
        )

    def test_set_neg_to_0_and_normalize(self):
        reactivities = [-2, -1, 0, 1, 2, 3]
        expected_reactivities = [0, 0, 0, 1/3, 2/3, 3/3]
        assert(
            Normalizers.set_neg_to_0_and_normalize(reactivities) == expected_reactivities
        )


    def test_align_sequence_with_reactivities(self):
        seq = "AACCCCUGGGAAACCC"
        reactivity_map = {
            4: 2.0,
            5: 1.2,
            6: -2.0,
            7: 0
        }

        expected_reactivity_map = {
            0: 0, 1: 0, 2: 0, 3: 0,
            4: 1.0, 5: 1.2/2, 6: 0, 7: 0,
            8: 0, 9: 0, 10: 0, 11: 0,
            12: 0, 13: 0, 14: 0, 15: 0
        }

        result = Normalizers.align_sequence_with_reactivities(seq, reactivity_map)
        assert(expected_reactivity_map == result)


    def test_detect_reactivity_dropoff_happy_path(self):
        seq = "CAAAACCAAAAAAU"
        reactivity_map = {
            1: 0.1, 2: 0.2, 3: 0.4, 4: 0.45,
            5: 0.5, 6: 1, 7: 1, 8: 1, 9: 1
        }
        spans_with_decreasing_reactivity = Normalizers.detect_reactivity_dropoff_in_polyA(seq, reactivity_map)
        expected_span = [[4, 3, 2, 1]]
        assert(spans_with_decreasing_reactivity == expected_span)

    def test_detect_reactivity_dropoff_w_no_dropoff(self):
        seq = "CAAAACCAAAAAAU"
        reactivity_map = {
            1: 0, 2: 0, 3: 0,
            4: 0, 5: 0, 6: 0,
            7: 0, 8: 0, 9: 0
        }

        spans_with_decreasing_reactivity = Normalizers.detect_reactivity_dropoff_in_polyA(seq, reactivity_map)
        expected_span = []
        assert(spans_with_decreasing_reactivity == expected_span)
