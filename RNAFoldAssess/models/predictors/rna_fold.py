import os


# Note that RNAFold is a tool found inside of ViennaRNA
# Since this work is using Vienna already, we're just going
# to use the local copy of its bin folder for this one

class RNAFold:
    def __int__(self):
        self.output = ""

    def execute(self, path, fasta_file):
        path_to_rna_fold = os.path.abspath(path)
        exec_string = f"{path} {fasta_file}"
        self.output = os.popen(exec_string).read()

    def get_ss_prediction(self):
        if self.output == "":
            raise Exception(f"RNAFold exception: no output generated")
        strings = self.output.split("\n")
        ss = strings[2]
        ss = ss.split()[0]
        return ss
