import os


class IPknot:
    def __init__(self):
        self.output = ""

    def execute(self, path, fasta_file, remove_file_when_done=False):
        path_to_ipknot = os.path.abspath(path)
        exec_string = f"{path_to_ipknot} {fasta_file}"
        self.output = os.popen(exec_string).read()
        if remove_file_when_done:
            os.remove(fasta_file)

    def get_ss_prediction(self):
        if self.output == "":
            raise Exception(f"IPknot exception: no output generated")
        strings = self.output.split("\n")
        ss = strings[-2]
        return ss

    def get_ss_prediction_ignore_pseudoknots(self):
        if self.output == "":
            raise Exception(f"IPknot exception: no output generated")
        strings = self.output.split("\n")
        ss = strings[-2]
        ss = ss.replace("[", ".").replace("]", ".")
        return ss