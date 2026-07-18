from Bio import Seq

class SecondaryStructureTools:
    MOTIF_KEY_PREFIXES = ["HELIX", "HAIRPIN", "LOOP", "MWAY", "5PER", "3PER"]

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


    @staticmethod
    def get_structural_motif_data(seq, stc):
        import forgi.graph.bulge_graph as fgb
        bg = fgb.BulgeGraph.from_dotbracket(stc)
        structure_data = bg.defines
        stc_motifs = {}
        for element, coords in structure_data.items():
            # make coords 0-indexed
            coords = [c - 1 for c in coords]
            if element.startswith("s"):
                # Helix/Stem
                s1b, s1e, s2b, s2e = coords
                s1_nts = "".join([seq[i] for i in range(s1b, s1e + 1)])
                s2_nts = "".join([seq[i] for i in range(s2b, s2e + 1)])
                s1_stc = "".join([stc[i] for i in range(s1b, s1e + 1)])
                s2_stc = "".join([stc[i] for i in range(s2b, s2e + 1)])
                key = f"HELIX_{s1_nts}&{s2_nts}_{s1_stc}&{s2_stc}"
            elif element.startswith("h"):
                # Hairpin
                nts = "".join([seq[i] for i in range(coords[0], coords[1] + 1)])
                structure = "".join([stc[i] for i in range(coords[0], coords[1] + 1)])
                key = f"HAIRPIN_{nts}_{structure}"
            elif element.startswith("i"):
                # Interior Loop
                s1b, s1e, s2b, s2e = coords
                s1_nts = "".join([seq[i] for i in range(s1b, s1e + 1)])
                s2_nts = "".join([seq[i] for i in range(s2b, s2e + 1)])
                s1_stc = "." * ((s1e + 1) - s1b)
                s2_stc = "." * ((s2e + 1) - s2b)
                key = f"LOOP_{s1_nts}&{s2_nts}_{s1_stc}&{s2_stc}"
            elif element.startswith("m"):
                # Multiway loops
                if coords == []:
                    key = f"MWAY_{element}_"
                else:
                    nts = "".join([seq[i] for i in coords])
                    bps = "".join([stc[i] for i in coords])
                    key = f"MWAY_{nts}_{bps}"
            elif element.startswith("f"):
                # five-prime exterior region
                nts = "".join(seq[i] for i in range(coords[0], coords[1] + 1))
                stcs = "".join(stc[i] for i in range(coords[0], coords[1] + 1))
                key = f"5PER_{nts}_{stcs}"
            elif element.startswith("t"):
                # three-prime exterior region
                nts = "".join(seq[i] for i in range(coords[0], coords[1] + 1))
                stcs = "".join(stc[i] for i in range(coords[0], coords[1] + 1))
                key = f"3PER_{nts}_{stcs}"

            stc_motifs[key] = coords

        return stc_motifs


    def get_gu_pairs(seq, stc):
        seq = seq.upper()
        pairings = SecondaryStructureTools.get_pairings(seq, stc)
        return pairings.count("GU") + pairings.count("UG")


    def get_motif_count(motif_type, motif_data):
        if motif_type not in SecondaryStructureTools.MOTIF_KEY_PREFIXES:
            raise SecondaryStructureToolsException(f"Unrecognized motif type: {motif_type}. Must be one of {SecondaryStructureTools.MOTIF_KEY_PREFIXES}")
        motifs = list(motif_data.keys())
        count = 0
        for m in motifs:
            if m.startswith(motif_type):
                count += 1
        return count

    def search_unpaired_nts_in_hairpin(hairpin, size_to_search_for=5):
        if not hairpin.startswith("HAIRPIN"):
            raise SecondaryStructureToolsException(f"This method only works on HAIRPIN motifs. You passed {hairpin}")
        stc = hairpin.split("_")[2]
        search_for = "." * size_to_search_for
        return search_for in stc


class SecondaryStructureToolsException(Exception):
    pass
