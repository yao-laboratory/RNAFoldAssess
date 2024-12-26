from .base_pair_scorer import BasePairScorer


class CanonicalBasePairScorer(BasePairScorer):
    ACCEPTABLE_PAIRS = [
        ('A', 'U'),
        ('U', 'A'),
        ('G', 'C'),
        ('C', 'G'),
        # Wobble pairs
        ('G', 'U'),
        ('U', 'G')
    ]

    def __init__(self, sequence, true_structure, predicted_structure, bp_lenience=0):
        transformed_structure = CanonicalBasePairScorer.transform_structure(true_structure, sequence)
        super().__init__(transformed_structure, predicted_structure, bp_lenience)


    @staticmethod
    def transform_structure(reference_structure, sequence):
        structure_coords = BasePairScorer.parse_structure(reference_structure)
        structure = list(reference_structure)
        for c1, c2 in structure_coords:
            bp = (sequence[c1], sequence[c2])
            if bp not in CanonicalBasePairScorer.ACCEPTABLE_PAIRS:
                structure[c1] = "."
                structure[c2] = "."
        return "".join(structure)