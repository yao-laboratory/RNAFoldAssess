import os


class ContraFold:
    def __init__(self):
        self.output = ""

    def execute(self, contra_path, seq_file, remove_file_when_done=False):
        # Note, ContraFold is just EternaFold with default params
        exec_string = f"{contra_path}/src/contrafold predict {seq_file}"
        self.output = os.popen(exec_string).read()
        if remove_file_when_done:
            # print(f"ContraFold object is deleting {seq_file}")
            os.remove(seq_file)

    def get_ss_prediction(self):
        if self.output == "":
            raise Exception(f"ContraFold exception: no output generated")
        strings = self.output.split("\n")
        ss = strings[2]
        return ss