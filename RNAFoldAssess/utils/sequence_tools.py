import math
from collections import Counter


class SequenceTools:
    @staticmethod
    def generate_kmers(sequence: str, k: int) -> list[str]:
        kmers = []
        for i in range(len(sequence) - k + 1):
            kmers.append(sequence[i:i+k])

        return kmers

    @staticmethod
    def count_homopolymers(sequence: str, k: int, nucleotide: str) -> int:
        kmers = SequenceTools.generate_kmers(sequence, k)
        kmer_to_find = nucleotide * k
        return kmers.count(kmer_to_find)

    @staticmethod
    def get_gc_content(sequence: str) -> float:
        g_count = sequence.upper().count("G")
        c_count = sequence.upper().count("C")
        return (g_count + c_count) / len(sequence)

    @staticmethod
    def get_sequence_entropy(sequence: str, log_base: int = 4) -> float:
        # Count nucleotide frequencies
        counts = Counter(sequence)
        total_bases = len(sequence)
        entropy = 0

        # Calculate entropy
        for count in counts.values():
            p = count / total_bases
            entropy -= p * math.log(p, log_base)
        return entropy

