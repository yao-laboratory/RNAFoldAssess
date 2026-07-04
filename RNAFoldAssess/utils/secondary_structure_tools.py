from Bio import Seq

class SecondaryStructureTools:
    @staticmethod
    def symmetric_chain(dbn: str, count_square_brackets: bool = False) -> bool:
        """
        Returns true if the given RNA chain is symmeteric. This
        is useful because most prediction models assume an input
        sequence is a whole molecule and thus will only predict
        base-pairs among the given sequence. For example, a
        molecule may be of two chains with the following secondary
        structure:

        ...(((..&..)))...

        The output of x3dna will return two chains from this
        secondary structure, neither of which will be symmetric:

        Chain 1 secondary structure:
        ...(((..
        Chain 2 secondary structure:
        ..)))...

        most (perhaps all) prediction algorithms cannot predict
        such a structure. If given the sequence to chain 1, a
        predictor will generate secondary structure predictions
        such as:

        ........
        ..(.)...
        (((..)))

        and so on. This method returns `False` if its input secondary
        structure string is not symmetric so that users can filter
        out un-predictable secondary structures from their data sets.
        """
        return dbn.count("(") == dbn.count(")")

    @staticmethod
    def contains_pseudoknots(dbn: str) -> bool:
        """
        Most dot-bracket schemas tends to use square brackets to
        annotate pseudoknots. Since many secondary structure prediction
        algorithms cannot predict pseudoknots, this method allows users
        to detect pseudoknots in their data sets.
        """
        return ("[" in dbn or "]" in dbn or "{" in dbn or "}" in dbn)

    @staticmethod
    def parse_structure(structure: str) -> list[tuple[int, int]]:
        """
        Return the 0-indexed coordinates of base pairs in a given
        secondary structure string.
        """
        # structure exampe: "..((((...))))..((..))."
        bps = []
        for i1, c1 in enumerate(structure):
            if c1 != '(':
                continue
            count = 1
            for i2, c2 in enumerate(structure[i1 + 1:]):
                if c2 == '(':
                    count += 1
                elif c2 == ')':
                    count -= 1
                    if count == 0:
                        bps.append((i1, i1 + i2 + 1))
                        break
        return bps

    @staticmethod
    def get_pairings(sequence: str, structure: str) -> list[str]:
        pair_coords = SecondaryStructureTools.parse_structure(structure)
        nts = [f"{sequence[x]}{sequence[y]}" for x, y in pair_coords]
        return nts

    @staticmethod
    def get_au_helix_end_pairs(motif):
        # Example: HELIX_GUGGC&GUCAC_(((((&)))))
        m_id, m_seq, m_stc = motif.split("_")
        if m_id != "HELIX":
            raise SecondaryStructureToolsException(f"This method only works on HELIX motifs. You passed {m_id}")
        pairs = SecondaryStructureTools.get_pairings(m_seq, m_stc)
        count = 0
        for pair in pairs:
            if pair not in ["AU", "UA"]:
                break
            count += 1

        for pair in pairs[::-1]:
            if pair not in ["AU", "UA"]:
                break
            count += 1

        if count > len(pairs):
            count = len(pairs)

        return count

    @staticmethod
    def helix_is_self_complementary_duplex(motif):
        # Example: HELIX_GUGGC&GUCAC_(((((&)))))
        m_id, m_seq, _m_stc = motif.split("_")
        if m_id != "HELIX":
            raise SecondaryStructureToolsException(f"This method only works on HELIX motifs. You passed {m_id}")

        seq1, seq2 = m_seq.split("&")
        reverse_complement = Seq.reverse_complement(seq2).replace("T", "U")
        return seq1 == reverse_complement


    @staticmethod
    def canonize_structure(seq, stc):
        acceptable_pairings = ["AU", "UA", "GC", "CG", "GU", "UG"]
        bps = SecondaryStructureTools.parse_structure(stc)
        stc = list(stc)
        for bp in bps:
            pair = f"{seq[bp[0]]}{seq[bp[1]]}"
            if pair not in acceptable_pairings:
                stc[bp[0]] = "."
                stc[bp[1]] = "."
        return "".join(stc)


class SecondaryStructureToolsException(Exception):
    pass
