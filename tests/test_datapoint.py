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
