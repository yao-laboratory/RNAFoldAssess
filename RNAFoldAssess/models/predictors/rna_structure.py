import os

from .predictor import Predictor


class RNAStructure(Predictor):
    """
    This model is an example of a predictor model wrapping a tool that must be used from
    the command line. RNAStructure utilizes a program called Fold that does not have any
    Python bindings (that we know of). This model also provides an example of wrapping a
    model whose prediction outputs a file and thus must be manipulated in order to get a
    dot-bracket notation (dbn) string. If you are building your own model that must wrap
    a tool that must be used from the command line, and/or produces an output other than
    a dbn string, please refer to this mdoel.

    NOTE: This model is provided as a reference for users. You **CANNOT** use this model
    if you haven't also already downloaded and installed the RNAStructure package.
    """

    def __init__(self, delete_seq_file=False):
        """
        In the `__init__` method, we pass a  `delete_seq_file` param that will be used
        to determine whether to delete the input file. Sometimes this is necessary as
        the input file may be generated on the fly from another source and the users do
        not want to crowd their directories with .seq files. To be safe, though, we set
        the default value for this param to `False`.
        """
        self.output = ""
        self.path_to_ct_file = ""
        self.delete_seq_file = delete_seq_file

    def execute(self,
                seq_file,
                path_to_rnastructure,
                output_path_base="rnastructure_outputs"):
        """
        The `execute` method takes a `path_to_rnastructure` parameter. This parameter is
        a string describing the path to rnastructure. For example: ./src/rnastrucutre.
        Inside this path should be, among other things, the `bin` folder. Because using
        this tool requires the following pattern from the command line:

            ./src/rnastructure/bin/Fold --MFE path/to/a/seq_file.seq path/to/output.ct

        We need to build the execution string as well as save the location of the output
        file so we can parse it later.

        This method builds an absolute path string to rnastructure's `Fold` program, the
        absolute path to a .ct file that will be created, and the builds the execution
        string from those values. The execution string is passed to `os.popen` and the
        output of that command is read into the `output` attribute of this class. Then,
        the class tries to delete the .seq file if the user instantiated this class with
        `delete_seq_file` as True. The path to the .ct file is saved in a class
        attribute called `path_to_ct_file` so that it can be parsed later in the
        `get_ss_prediction` and `get_mfe` methods.
        """

        self.path_to_rnastructure = os.path.abspath(path_to_rnastructure)

        sfile_name = os.path.basename(seq_file)
        fold_path = f"{self.path_to_rnastructure}/bin/Fold"

        ct_name = f"{sfile_name.split('.')[0]}.ct"
        self.path_to_ct_file = f"{output_path_base}/{ct_name}"

        exec_string = f"{fold_path} --MFE {os.path.abspath(seq_file)} {self.path_to_ct_file}"
        self.output = os.popen(exec_string).read()

        if self.delete_seq_file:
            try:
                os.remove(seq_file)
            except FileNotFoundError:
                print(f"RNAStructure: Couldn't find {seq_file} files to delete")

    def get_ss_prediction(self):
        """
        Since RNAStructure generates a .ct file as a secondary structure prediction, the
        output needs to be translated to a dbn string. To do this, we make use of the
        ct2db program that comes iwth RNAStructure. We use this program by building an
        absolute path to it and constructing an execution string from that and the saved
        path to the generated .ct file in the `path_to_ct_file` attribute. We pass that
        execution string to `os.popen` and read and parse the output to return the dbn.
        """

        if not os.path.isfile(self.path_to_ct_file):
            raise Exception(f"RNAStructure exception: no .ct file generated")

        ct2db_path = f"{self.path_to_rnastructure}/bin/ct2db"
        exec_string = f"{ct2db_path} {self.path_to_ct_file}"
        output = os.popen(exec_string).read()
        strings = output.split("\n")
        ss = strings[2]
        return ss

    def get_mfe(self):
        """
        The `Fold` program outputs a .ct file as its prediction and records the
        minimum free energy (MFE) of the prediction in that file. Therefore, this method
        parses the generated .ct file and reads the MFE value from it, the returns that
        value, casted as a float. If the MFE can't be found, we return `None` here.
        """
        f = open(self.path_to_ct_file)
        data = f.readlines()
        f.close()
        first_line = data[0]
        strings = first_line.split()
        if len(strings) > 3:
            mfe = strings[3]
            return float(mfe)
        else:
            return None

    def delete_ct_file(self):
        """
        This method is provided as a convenience method to the user. Because the tool
        produces a .ct file as a prediction, it is possible there will be several .ct
        files generated in a pipeline with lots of predictions. As such, we provide this
        method to make cleaning up those files a little easier.
        """
        try:
            os.remove(self.path_to_ct_file)
        except FileNotFoundError:
            print(f"RNAStructure couldn't find {self.path_to_ct_file} to delete")
