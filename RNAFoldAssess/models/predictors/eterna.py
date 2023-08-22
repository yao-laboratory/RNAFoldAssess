import os


class Eterna:
    def __init__(self):
        self.output = ""

    def execute(self, eterna_path, seq_file, remove_file_when_done=True):
        exec_string = f"{eterna_path}/src/contrafold predict {seq_file} --params {eterna_path}/parameters/EternaFoldParams.v1"
        self.output = os.popen(exec_string).read()
        if remove_file_when_done:
            print(f"Eterna object is deleting {seq_file}")
            os.remove(seq_file)

    def get_ss_prediction(self):
        if self.output == "":
            raise Exception(f"EternaFold exception: no output generated")
        strings = self.output.split("\n")
        ss = strings[strings.index('>structure') + 1]
        return ss
