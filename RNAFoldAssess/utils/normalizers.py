import re

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

    @staticmethod
    def normalize_from_reactivity_map(reactivity_map):
        new_vals = Normalizers.set_neg_to_0_and_normalize(list(reactivity_map.values()))
        new_map = {}
        for i, pos in enumerate(reactivity_map.keys()):
            new_map[pos] = new_vals[i]
        return new_map

    @staticmethod
    def align_sequence_with_reactivities(sequence, reactivity_map):
        normalized_map = Normalizers.normalize_from_reactivity_map(reactivity_map)
        new_reactivity_map = {}
        for i in range(len(sequence)):
            if i not in normalized_map:
                new_reactivity_map[i] = 0
            else:
                new_reactivity_map[i] = normalized_map[i]
        return new_reactivity_map


    @staticmethod
    def detect_reactivity_dropoff_in_polyA(sequence, reactivity_map, a_length=4):
        a_string = "A" * a_length
        regex = rf'(?=({re.escape(a_string)}))'
        spans = [(m.start(1), m.start(1) + 4) for m in re.finditer(regex, sequence)]
        reactivities_to_test = []
        for span in spans:
            full_span = list(range(span[0], span[1]))
            reactivities_to_test.append(
                [reactivity_map.get(i, None) for i in full_span]
            )

        # Since we're going from 5' to 3', we are testing for *increasing* values
        # because that would be the same decresing values in the 3' to 5' direction
        spans_with_increasing_reactivity = []
        for r_index, rtt in enumerate(reactivities_to_test):
            increases_in_a_row = 0
            for i, reac in enumerate(rtt):
                if i == len(rtt) - 1:
                    break
                if reac is None or rtt[i+1] is None:
                    continue
                if reac >= rtt[i+1]:
                    break
                else:
                    increases_in_a_row += 1
            if increases_in_a_row >= 3:
                spans_with_increasing_reactivity.append(
                    list(range(spans[r_index][0], spans[r_index][1]))
                )

        spans_with_decreasing_reactivity = [span[::-1] for span in spans_with_increasing_reactivity]
        return spans_with_decreasing_reactivity
