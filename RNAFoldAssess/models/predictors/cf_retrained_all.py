import os


class ContraRetrainedAll:
    def __init__(self):
        self.output = ""

    def execute(self, contra_path, seq_file, remove_file_when_done=False):
        exec_string = f"{contra_path}/src/contrafold predict {seq_file} --params /common/yesselmanlab/ewhiting/data/bprna/retrain_all/optimize.params.iter17"
        self.output = os.popen(exec_string).read()
        if remove_file_when_done:
            # print(f"Eterna object is deleting {seq_file}")
            os.remove(seq_file)

    def get_ss_prediction(self):
        if self.output == "":
            raise Exception(f"ContraRetrained exception: no output generated")
        strings = self.output.split("\n")
        ss = strings[strings.index('>structure') + 1]
        return ss
