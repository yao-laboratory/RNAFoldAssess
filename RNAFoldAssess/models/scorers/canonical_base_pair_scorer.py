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

    SPECIAL_CHAR_MAP = {
        ".": ".", "(": "(", ")": ")",
        "{": ".", "}": ".", "[": ".", "]": ".",
        "<": "(", ">": ")"
    }

    def __init__(self, sequence, true_structure, predicted_structure, bp_lenience=0):
        transformed_structure = CanonicalBasePairScorer.transform_structure(true_structure, sequence)
        super().__init__(transformed_structure, predicted_structure, bp_lenience)


    @staticmethod
    def translate_special_character(nt):
        if nt in CanonicalBasePairScorer.SPECIAL_CHAR_MAP:
            return CanonicalBasePairScorer.SPECIAL_CHAR_MAP[nt]
        else:
            return "."


    @staticmethod
    def transform_structure(reference_structure, sequence):
        reference_structure = CanonicalBasePairScorer.remove_special_characters(reference_structure)
        structure_coords = BasePairScorer.parse_structure(reference_structure)
        structure = list(reference_structure)
        for c1, c2 in structure_coords:
            bp = (sequence[c1], sequence[c2])
            if bp not in CanonicalBasePairScorer.ACCEPTABLE_PAIRS:
                structure[c1] = "."
                structure[c2] = "."
        return "".join(structure)
    

    @staticmethod
    def remove_special_characters(stc):
        stc = list(stc)
        try:
            for i in range(len(stc)):
                nt = CanonicalBasePairScorer.translate_special_character(stc[i])
                stc[i] = nt
        except Exception as e:
            breakpoint()
        return "".join(stc)
