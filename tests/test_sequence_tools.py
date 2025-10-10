import pytest

from RNAFoldAssess.utils import SequenceTools


class TestKMerMethod:
    def test_find_3mers(self):
        sequence = "ACCUGAG"
        kmers = SequenceTools.generate_kmers(sequence, 3)
        expected_3mers = [
            "ACC", "CCU", "CUG", "UGA", "GAG"
        ]
        # Make sure there are no extras
        assert(len(expected_3mers) == len(kmers))
        # Make sure expected kmers are generated
        for kmer in expected_3mers:
            assert(kmer in kmers)

    def test_count_homopolymers(self):
        sequence = "AAAAAA"
        homopolymer_count = SequenceTools.count_homopolymers(sequence, 3, "A")
        assert(homopolymer_count == 4)
