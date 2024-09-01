import os


class CFRetrainedEterna:
    def __init__(self):
        self.output = ""

    def execute(self, contra_path, seq_file, remove_file_when_done=False):
        exec_string = f"{contra_path}/src/contrafold predict {seq_file} --params /work/yesselmanlab/ewhiting/chem_map_to_bpseq/retrainings/eterna/optimize.params.iter70"
        self.output = os.popen(exec_string).read()
        if remove_file_when_done:
            os.remove(seq_file)

    def get_ss_prediction(self):
        if self.output == "":
            raise Exception(f"CFRetrainedEterna exception: no output generated")
        strings = self.output.split("\n")
        ss = strings[2]
        return ss
