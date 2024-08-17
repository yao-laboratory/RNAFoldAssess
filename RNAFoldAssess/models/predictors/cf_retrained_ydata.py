import os


class ContraRetrainedYData:
    def __init__(self):
        self.output = ""

    def execute(self, contra_path, seq_file, remove_file_when_done=False):
        param_file = "/work/yesselmanlab/ewhiting/chem_map_to_bpseq/retrainings/ydata/optimize.params.iter65"
        exec_string = f"{contra_path}/src/contrafold predict {seq_file} --params {param_file}"
        self.output = os.popen(exec_string).read()
        if remove_file_when_done:
            # print(f"Eterna object is deleting {seq_file}")
            os.remove(seq_file)

    def get_ss_prediction(self):
        if self.output == "":
            raise Exception(f"ContraRetrained exception: no output generated")
        strings = self.output.split("\n")
        ss = strings[2]
        return ss
