import os


class SPOT_RNA:
    def __init__(self, conda_env_name="spot"):
        self.output = ""
        # self.ct2db_path_string = "../ViennaRNA-2.6.2/src/Utils/ct2db"
        self.ct2db_path_string = "/home/yesselmanlab/ewhiting/ViennaRNA/src/Utils/ct2db"
        self.conda_env_name = conda_env_name

    def execute(self, spot_rna_path, fasta_file, remove_file_when_done=False):
        # Make output directory for SPOT
        if not os.path.exists("./spot_output"):
            os.mkdir("./spot_output")
        spot_exec_string = f"python3 {spot_rna_path}/SPOT-RNA.py  --inputs {fasta_file}  --outputs ./spot_output"
        # SPOT-RNA generates several files, we need the  .ct file
        # to get the secondary structure in dot-bracket notation
        conda_exec_string = f"conda run -n {self.conda_env_name} {spot_exec_string}"
        os.system(conda_exec_string)
        ct_file = fasta_file.split('/')[-1].replace('fasta', 'ct')
        ct_file_path = os.path.abspath(f"spot_output/{ct_file}")
        # Now we need to use the Vienna ct2db tool to
        # get the output in the format we want
        ct2db_exec_string = f"{self.ct2db_path_string} {str(ct_file_path)}"
        self.output = os.popen(ct2db_exec_string).read()
        if remove_file_when_done:
            os.remove(fasta_file)

    def get_ss_prediction(self):
        if self.output == "":
            raise Exception(f"SPOT-RNA exception: no output generated")
        strings = self.output.split("\n")
        ss = strings[-2]
        return ss
