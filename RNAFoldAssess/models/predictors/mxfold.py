import os


class MXFold:
    def __int__(self):
        self.output = ""

    def execute(self, path, fasta_file):
        path_to_mx_fold = os.path.abspath(path)
        exec_string = f"{path} {fasta_file}"
        self.output = os.popen(exec_string).read()

    def get_ss_prediction(self):
        if self.output == "":
            raise Exception(f"MXFold exception: no output generated")
        strings = self.output.split("\n")
        ss = strings[3]
        return ss
