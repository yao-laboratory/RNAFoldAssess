import os
import subprocess


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


class SPOT_RNA:
    def __init__(self, conda_env_name="spot"):
        self.output = ""
        # self.ct2db_path_string = "../ViennaRNA-2.6.2/src/Utils/ct2db"
        self.ct2db_path_string = "../ViennaRNA/src/Utils/ct2db"
        self.conda_env_name = conda_env_name

    def execute(self, spot_rna_path, fasta_file, remove_file_when_done=False):
        # Make output directory for SPOT
        if not os.path.exists("./spot_output"):
            os.mkdir("./spot_output")
        spot_exec_string = f"python3 {spot_rna_path}/SPOT-RNA.py  --inputs {fasta_file}  --outputs ./spot_output"
        print(f"spot_exec_string: {spot_exec_string}")
        # SPOT-RNA generates several files, we need the  .ct file
        # to get the secondary structure in dot-bracket notation
        conda_exec_string = f"conda run -n {self.conda_env_name} {spot_exec_string}"
        print(f"\nRunning {conda_exec_string}")
        os.system(conda_exec_string)
        ct_file = fasta_file.split('/')[-1].replace('fasta', 'ct')
        ct_file_path = os.path.abspath(f"spot_output/{ct_file}")
        # Now we need to use the Vienna ct2db tool to
        # get the output in the format we want
        ct2db_exec_string = f"{self.ct2db_path_string} {str(ct_file_path)}"
        print(f"\nRunning {ct2db_exec_string}")
        self.output = os.popen(ct2db_exec_string).read()
        if remove_file_when_done:
            print(f"SPOT-RNA object is deleting {fasta_file}")
            os.remove(fasta_file)

    def get_ss_prediction(self):
        if self.output == "":
            raise Exception(f"SPOT-RNA exception: no output generated")
        strings = self.output.split("\n")
        ss = strings[-2]
        return ss


class ContextFold:
    # If running on UNL HCC Swan, make sure to run `module load java`
    def __init__(self):
        self.output = ""

    def execute(self, cf_path, sequence):
        # Working with just a sequence for now, maybe we'll have to add
        # the ability to work with files. It only takes .txt files
        path_to_context_fold = os.path.abspath(cf_path)
        #  cd ContextFold_1_00 && java -cp bin contextFold.app.Predict in:AAGGCCUUGGGGAAGGCCUU && cd ..
        exec_string = f"cd {path_to_context_fold} && java -cp bin contextFold.app.Predict in:{sequence} && cd .."
        self.output = os.popen(exec_string).read()

    def get_ss_prediction(self):
        if self.output == "":
            raise Exception(f"ContextFold exception: no output generated")
        strings = self.output.split("\n")
        ss = strings[1]
        return ss


class DeepFoldRNA:
    # Some notes
    # This one might not be doable, there is 500GB of data to download
    # Also needs pytorch :(
    # Notes
    # Need to first run
    # ```
    #   source scripts/activate_conda_env.sh
    # ```
    #
    # For the number of threads, run
    # ```
    #   export OMP_NUM_THREADS=n
    # ```
    #
    # The input is a fasta file in a directory
    def __init__(self):
        output = ""


class MXFold:
    def __int__(self):
        self.output = ""

    def execute(self, path, fasta_file):
        path_to_mx_fold = os.path.abspath(path)
        exec_string = f"{path} {fasta_file}"
        self.output = os.popen(exec_string).read()

    def get_ss_prediction(self):
        if self.output == "":
            raise Exception(f"MXFold exception: no output generated")
        strings = self.output.split("\n")
        ss = strings[3]
        return ss
