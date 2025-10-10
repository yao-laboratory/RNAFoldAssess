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
        bp_sym = dbn.count("(") == dbn.count(")")
        if count_square_brackets:
            pseudoknot_sym = dbn.count("[") == dbn.count("]")
            return bp_sym and pseudoknot_sym
        else:
            return bp_sym

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


class SecondaryStructureToolsException(Exception):
    pass
