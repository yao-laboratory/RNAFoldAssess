import os


class MXFold2:
    # Note: I compiled MXFold2 with pytorch 1.5.1, so I may have to ensure
    # that I run `conda load pytorch/1.5.1` when running this.
    def __init__(self):
        self.output = ""

    def execute(self, fasta_file, path="", remove_file_when_done=True):
        if path == "":
            path = "/home/yesselmanlab/ewhiting/.conda/envs/rna_fold_assess/bin/mxfold2"
        exec_string = f"{path} predict {fasta_file}"
        self.output = os.popen(exec_string).read()
        if remove_file_when_done:
            try:
                os.remove(fasta_file)
            except FileNotFoundError:
                print(f"MXfold2: Couldn't find {fasta_file} to delete")

    def get_ss_prediction(self):
        if self.output == "":
            raise Exception(f"MXFold2 exception: no output generated")
        strings = self.output.split("\n")
        prediction = strings[2]
        spl = prediction.split(" ")
        ss = spl[0]
        return ss

    def get_fe_of_prediction(self):
        if self.output == "":
            raise Exception(f"MXFold2 exception: no output generated")
        strings = self.output.split("\n")
        prediction = strings[2]
        spl = prediction.split(" ")
        ss = spl[0]
        fe = spl[1]
        fe = float(fe.replace("(", "").replace(")", ""))
        return fe
