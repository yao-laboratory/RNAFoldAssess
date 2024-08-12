import os


# Note that RNAFold is a tool found inside of ViennaRNA
# Since this work is using Vienna already, we're just going
# to use the local copy of its bin folder for this one.

class RNAFold:
    def __int__(self):
        self.output = ""

    def execute(self, path, fasta_file, remove_file_when_done=True):
        # Overwrite any path passed to this model and use the
        # local one loaded by `module load viennarna`.
        path = "RNAfold"
        exec_string = f"{path} -i {fasta_file}"
        self.output = os.popen(exec_string).read()
        file_name_base = fasta_file.split(".")[0]
        try:
            os.remove(f"{file_name_base}.ps")
        except FileNotFoundError:
            print(f"Couln't delete {file_name_base}.ps")
        if remove_file_when_done:
            try:
                os.system(f"rm {file_name_base}*")
            except FileNotFoundError:
                print(f"RNAFold: Couldn't find {file_name_base} files to delete")

    def get_ss_prediction(self):
        if self.output == "":
            raise Exception(f"RNAFold exception: no output generated. Is viennarna loaded?")
        strings = self.output.split("\n")
        ss = strings[2]
        ss = ss.split()[0]
        return ss

    def get_prediction_fe(self):
        if self.output == "":
            raise Exception(f"RNAFold exception: no output generated. Is viennarna loaded?")
        strings = self.output.split("\n")
        fe = strings[2]
        fe = fe.split()[-1]
        fe = float(fe.replace("(", "").replace(")", ""))
        return fe
