import os


# Note that RNAFold is a tool found inside of ViennaRNA
# Since this work is using Vienna already, we're just going
# to use the local copy of its bin folder for this one

class RNAFold:
    def __int__(self):
        self.output = ""

    def execute(self, path, fasta_file, delete_input_file_immediately=True):
        path_to_rna_fold = os.path.abspath(path)
        exec_string = f"{path} {fasta_file}"
        self.output = os.popen(exec_string).read()
        file_name_base = fasta_file.split(".")[0]
        if delete_input_file_immediately:
            os.system(f"rm {file_name_base}*")

    def get_ss_prediction(self):
        if self.output == "":
            raise Exception(f"RNAFold exception: no output generated. Is Java in the path?")
        strings = self.output.split("\n")
        ss = strings[2]
        ss = ss.split()[0]
        return ss
