import os


class RandomPredictor:
    def __init__(self):
        self.output = ""

    def execute(self, fasta_file, path="/home/yesselmanlab/ewhiting/EternaFold/src/contrafold"):
        sampler = f"{path} sample"
        f = open("ss_file.txt", "w")
        f.close()
        cmd = f"{sampler} {fasta_file} --nsamples 1 >> ss_file.txt"
        os.system(cmd)
        f2 = open("ss_file.txt", "r")
        self.output = f2.read().strip()
        f2.close()
        # os.remove("ss_file.txt")

    def get_ss_prediction(self):
        if self.output == "":
            raise Exception("RandomPredictor exception: no output generated")
        return self.output
