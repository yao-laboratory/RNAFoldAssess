import os


class MXFold2RetrainedCurated:
    def __init__(self):
        self.output = ""
        base_dir = "/work/yesselmanlab/ewhiting/chem_map_to_bpseq/retrainings"
        self.path_to_model = f"{base_dir}/retrain_mxfold2/curated/model_all.conf"

    def execute(self, fasta_file, path="", remove_file_when_done=False):
        if path == "":
            path = "/common/yesselmanlab/ewhiting/.conda/envs/mxfold2_env/bin/mxfold2"
        exec_string = f"{path} predict @{self.path_to_model} {fasta_file}"
        self.output = os.popen(exec_string).read()
        if remove_file_when_done:
            try:
                os.remove(fasta_file)
            except FileNotFoundError:
                print(f"MXFold2RetrainedCurated: Couldn't find {fasta_file} to delete")

    def get_ss_prediction(self):
        if self.output == "":
            raise Exception(f"MXFold2RetrainedCurated exception: no output generated")
        strings = self.output.split("\n")
        prediction = strings[2]
        spl = prediction.split(" ")
        ss = spl[0]
        return ss

    def get_fe_of_prediction(self):
        if self.output == "":
            raise Exception(f"MXFold2RetrainedCurated exception: no output generated")
        strings = self.output.split("\n")
        prediction = strings[2]
        spl = prediction.split(" ")
        ss = spl[0]
        fe = spl[1]
        fe = float(fe.replace("(", "").replace(")", ""))
        return fe
