import os


class CFRetrainedRibonanza:
    def __init__(self):
        self.output = ""

    def execute(self, contra_path, seq_file, remove_file_when_done=False):
        exec_string = f"{contra_path}/src/contrafold predict {seq_file} --params /work/yesselmanlab/ewhiting/chem_map_to_bpseq/retrainings/ribonanza/optimize.params.iter71"
        self.output = os.popen(exec_string).read()
        if remove_file_when_done:
            # print(f"Eterna object is deleting {seq_file}")
            os.remove(seq_file)

    def get_ss_prediction(self):
        if self.output == "":
            raise Exception(f"CFRetrainedRibonanza exception: no output generated")
        strings = self.output.split("\n")
        ss = strings[2]
        return ss
