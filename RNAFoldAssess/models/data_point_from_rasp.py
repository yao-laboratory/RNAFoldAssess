import json

from RNAFoldAssess.models import DataPoint


class DataPointFromRASP(DataPoint):
    def __init__(self, data_hash, cohort=None, normalize_reactivities_on_init=False):
        if "coordinates" in list(data_hash.keys()):
            self.coordinates = data_hash["coordinates"]
        super().__init__(data_hash, cohort, normalize_reactivities_on_init)

    @staticmethod
    def factory(path, name_prefix=None):
        f = open(path)
        json_data = json.loads(f.read())
        f.close()
        data_points = []
        for datum in json_data:
            data_points.append(DataPointFromRASP(datum, name_prefix))
        return data_points
