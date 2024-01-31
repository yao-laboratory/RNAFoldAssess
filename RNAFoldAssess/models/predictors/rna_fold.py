import os


class RNAFold:
    """
    This predictor model is provided as an example, but is capable of being
    used as well. In order to use the RNAFold predictor class, you must first
    install the ViennaRNA package. Installation instructions for this package
    can be found at the following link:

        https://www.tbi.univie.ac.at/RNA/ViennaRNA/doc/html/install.html

    Once you have ViennaRNA installed, you have access to RNAFold. You will
    use the path to the RNAFold executable when running the `execute` method
    of this class.

    To make a prediction with the RNAFold class from a FASTA file, consider
    the following example code:

    ```python
    model = RNAFold()
    path_to_rnafold_binary = os.path.abspath("/home/user/tools/ViennaRNA/bin/RNAfold")
    fasta_file_path = os.path.abspath("/home/user/data/some_rna_file.fasta")

    model.execute(path_to_rnafold_binary, fasta_file_path)
    prediction = model.get_ss_prediction()
    ```

    Note that running `execute` sets the model's `output` attribute to the
    predicted secondary structure in dot-bracket notation. To retrieve that
    dot-bracket string, you have to run the `get_ss_prediction` method.
    """
    def __init__(self):
        self.output = ""

    def execute(self, path_to_rnafold, fasta_file, remove_file_when_done=False):
        exec_string = f"{path_to_rnafold} {fasta_file}"
        self.output = os.popen(exec_string).read()
        file_name_base = fasta_file.split(".")[0]
        if remove_file_when_done:
            try:
                os.system(f"rm {file_name_base}*")
            except FileNotFoundError:
                print(f"RNAFold: Couldn't find {file_name_base} files to delete")

    def get_ss_prediction(self):
        if self.output == "":
            # Please note that RNAFold requires Java in the path
            raise Exception(f"RNAFold exception: no output generated. Is Java in the path?")
        strings = self.output.split("\n")
        ss = strings[2]
        ss = ss.split()[0]
        return ss
