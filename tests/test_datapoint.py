import pytest

from RNAFoldAssess.models import DataPoint


class TestConstructorGetterSetters:
    name = "test_sequence1"
    sequence = "AACCUAACCGAACUUU"
    ground_truth_data = [
        0.5, 0.5, 0.6, 0.6,
        0.0, 0.1, 0.1, 0.5,
        0.1, 0.0, 0.6, 0.7,
        0.9, 0.0, 0.0, 0.0
    ]

    def constructor_happy_path(self):
        ground_truth_type = "DMS"

        try:
            DataPoint(self.name, self.sequence, ground_truth_type, self.ground_truth_data)
        except Exception as e:
            pytest.fail(f"Unexepected exception raised: {e}")

    def test_constructor_reject_ground_truth(self):
        bad_ground_truth = "dimethyl sulfate"
        with pytest.raises(Exception) as exception_info:
            DataPoint(self.name, self.sequence, bad_ground_truth, self.ground_truth_data)

        assert str(exception_info.value) == f"The ground-truth type {bad_ground_truth} is not acceptable, must be one of {DataPoint.ACCEPTABLE_GROUND_TRUTH_TYPES}"

    def test_reactivities_getter_no_reactivities(self):
        dp = DataPoint(self.name, self.sequence, "SHAPE")
        with pytest.raises(Exception) as exception_info:
            dp.reactivities

        assert str(exception_info.value) == f"Datapoint {self.name} does not have reactivities"

    def test_reactivities_getter_gt_is_dbn(self):
        dp = DataPoint(self.name, self.sequence, "DBN", "((((....))))")
        with pytest.raises(Exception) as exception_info:
            dp.reactivities

        assert str(exception_info.value) == f"Datapoint {self.name} does not have reactivities"

class TestConstructFrom:
    name = "test"
    seq = "AACCUUGG"
    data = "..((..))"
    good_dict_data = {
        "name": name,
        "sequence": seq,
        "dbn": data
    }

    def test_construct_from_dictionary(self):
        dp = DataPoint.init_from_dict(self.good_dict_data)
        assert dp.name == self.name
        assert dp.sequence == self.seq
        assert dp.structure == self.data

class TestReactivityMap:
    name = "test"
    seq = "AACCUUGG"
    full_reactivity_map = {
        0: 0.4,
        1: 0.5,
        2: 0.7,
        3: 0.6,
        4: 0.0,
        5: 0.1,
        6: 0.2,
        7: 0.3,
    }

    partial_reactivit_map = {3: 0.9, 4: 0.0, 7: 0.1}

    def test_reactivities_from_map(self):
        dp = DataPoint(self.name, self.seq, "DMS", self.full_reactivity_map)
        expected_reactivities = [0.4, 0.5, 0.7, 0.6, 0.0, 0.1, 0.2, 0.3]
        assert dp.reactivities == expected_reactivities
        assert dp.reactivity_map == self.full_reactivity_map

    def test_partial_reactivity_map(self):
        dp = DataPoint(self.name, self.seq, "DMS", self.partial_reactivit_map)
        expected_reactivities = [0.9, 0.0, 0.1]
        assert dp.reactivities == expected_reactivities
        assert dp.reactivity_map == self.partial_reactivit_map

    def test_bad_list(self):
        with pytest.raises(Exception) as exception_info:
            DataPoint(self.name, self.seq, "DMS", [1,2,3])

        expected_error_info = f"DataPoint: {self.name}\nSequence: {self.seq}\nProvided reactivities: [1, 2, 3]"
        assert expected_error_info in str(exception_info.value)

    def test_bad_dict(self):
        with pytest.raises(Exception) as exception_info:
            DataPoint(self.name, self.seq, "DMS", {0: 1, 1:2, 10: 4})

        expected_error_info = f"Encountered position 10 for sequence of length {len(self.seq)}"
        assert expected_error_info in str(exception_info.value)

