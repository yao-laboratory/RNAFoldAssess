class Normalizers:
    """
    Utitlities for normalizing data. This is mostly for normalizing
    DMS and SHAPE readings. To normalize, we usually divide everything
    by the highest number in the dataset. Also, we sometimes have to
    change negative numbers to just be zero
    """

    @staticmethod
    def simple_normalizer(data=[]):
        m = max(data)
        return [float(d) / m for d in data]

    @staticmethod
    def set_neg_to_0_and_normalize(data=[]):
        for i, v in enumerate(data):
            if v < 0:
                data[i] = 0
        return Normalizers.simple_normalizer(data)