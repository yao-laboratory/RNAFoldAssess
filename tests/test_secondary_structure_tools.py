from RNAFoldAssess.utils import SecondaryStructureTools


class TestGetPairingMethod:
    def test_get_pairings(self):
        stc = "...(((.....)))..."
        seq = "GGGCAGACCUGUUGAUU"
        expectation = ["CG", "AU", "GU"]
        base_pairs = SecondaryStructureTools.get_pairings(seq, stc)
        assert(expectation == base_pairs)

