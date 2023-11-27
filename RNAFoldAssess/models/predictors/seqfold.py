import os


class SeqFold:
    # If running on UNL HCC Swan, make sure the right conda environment is loaded
    def __init__(self):
        self.output = ""

    def execute(self, path_to_executable, sequence):
        # This tool only needs a sequence, no files
        path_to_executable = os.path.abspath(path_to_executable)
        exec_string = f"{path_to_executable} -d {sequence}"
        self.output = os.popen(exec_string).read()

    def get_ss_prediction(self):
        if self.output == "":
            raise Exception("SeqFold exception: no output generated")
        strings = self.output.split("\n")
        ss = strings[1]
        return ss
