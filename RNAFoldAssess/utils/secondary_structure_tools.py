import os, string, random


class SecondaryStructureTools:
    asterisks  = "*" * 76
    ss_string = "Secondary structures"

    @staticmethod
    def parse_structure_file(path):
        """
        # This method parses the standard-output generated from the
        # x3dna DSSR method. Usually, we just use the files output
        # by that tool, but sometimes we pipe the entire output to
        # a file. This method can read such a file and return an
        # object from it. The object is a Python dictionary object
        # with name, sequence, structure, and chains key-value pairs.
        """
        f = open(path)
        raw_data = f.read()
        data = raw_data.split(SecondaryStructureTools.asterisks)
        ss_data = None
        for d in data:
            if SecondaryStructureTools.ss_string in d:
                ss_data = d
                break
        if not ss_data:
            raise SecondaryStructureToolsException(f"No secondary structure in {path}")
        ss_data = ss_data.split("\n")
        whole_seq = ""
        whole_structure = ""
        chains = []
        for i in range(len(ss_data)):
            if "[whole]" in ss_data[i]:
                whole_seq = ss_data[i+1]
                whole_structure = ss_data[i+2]
            if "[chain]" in ss_data[i]:
                chain_id = ss_data[i].split("-")[1].split(" ")[0]
                chains.append({
                    "chain_id": chain_id,
                    "sequence": ss_data[i+1],
                    "structure": ss_data[i+2]
                })
        return {
            "name": path.split(".")[0].split("/")[-1],
            "sequence": whole_seq,
            "structure": whole_structure,
            "chains": chains
        }

    @staticmethod
    def symmetric_chain(dbn, count_square_brackets=False):
        """
        Returns true if the given RNA chain is symmeteric. This
        is useful because most prediction models assume an input
        sequence is a whole molecule and thus will only predict
        base-pairs among the given sequence. For example, a
        molecule may be of two chains with the following secondary
        structure:

        ...(((..&..)))...

        The output of x3dna and the `parse_structure_file` method
        above will return two chains from this secondary structure,
        neither of which will be symmetric:

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
        if count_square_brackets:
            dbn = dbn.replace("[", "(").replace("]", ")")
        return dbn.count("(") == dbn.count(")")

    @staticmethod
    def contains_pseudoknots(dbn):
        """
        Most dot-bracket schemas tends to use square brackets to
        annotate pseudoknots. Since many secondary structure prediction
        algorithms cannot predict pseudoknots, this method allows users
        to detect pseudoknots in their data sets.
        """
        return ("[" in dbn or "]" in dbn)

    @staticmethod
    def get_free_energy(sequence, structure):
        rna_fold_path = "/home/yesselmanlab/ewhiting/ViennaRNA/bin/RNAeval"
        # Have to make temp file
        random_string = "".join(random.choices(string.ascii_letters + string.digits, k=12))
        tmp_file = f"/common/yesselmanlab/ewhiting/tmp/input_{random_string}.txt"
        fh = open(tmp_file, "w")
        fh.write(f"{sequence}\n{structure}")
        fh.close()
        # The `--nsp` allows for non-canonical base pairs
        cmd = f'{rna_fold_path} --nsp="CU,UC,AC,CA,AG,GA,GG,AA,UU,CC" -d2 < {tmp_file}'
        fe_output = os.popen(cmd).read().strip()
        if fe_output == "":
            return False
        fe = fe_output.split(" ")[-1]
        fe = float(fe.replace("(", "").replace(")", ""))
        try:
            os.remove(tmp_file)
        except FileNotFoundError:
            print(f"SecondaryStructureTools couldn't remove {tmp_file}")
            return fe
        return fe

    @staticmethod
    def ct2db(ct_file_path):
        # The vienna binaris are so finnicky, I'm just implementing this myself
        f = open(ct_file_path)
        data = f.readlines()
        f.close()

        data = data[4:-1]
        data = [d.split() for d in data]
        seq = "".join([s[1] for s in data])

        dbn = ["." for _ in range(len(seq))]
        pairs = [(int(d[2]), int(d[4]) - 1) for d in data if d[4] != "0"]
        pairs = [p for p in pairs if p[0] < p[1]]

        for p in pairs:
            db = dbn[p[0]]
            if db == ".":
                dbn[p[0]] = "("
                dbn[p[1]] = ")"

        dbn = "".join(dbn)

        return dbn


class SecondaryStructureToolsException(Exception):
    pass
