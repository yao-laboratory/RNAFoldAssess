import ViennaRNA

from .predictor import Predictor


class RNAFold(Predictor):
    """
    This class is provided as an example and for the convenience of the user. The
    RNAFold tool is present in the ViennaRNA package from PyPI, so we install it here.
    If you would rather use a local installation, you will have to make a new class
    and call the tool from there, probably with `os.system(<execution string>)` or
    something like that.

    Assuming you have install the necessary requirements, you can use this class
    as follows:
        1. Instantiate an `RNAFold` object
        2. Call the `execute` method, passing it a `DataPoint` object
        3. To get the secondary structure prediction after execution:
            a. Use the `get_ss_prediction` method. This will return a dot-bracket
               notation (dbn) string of the prediction.
            b. If the `execute` method failed for some reason besides a missing file
               path. The `get_ss_prediction` method will raise an
               `RNAFoldExecutionException`
    """

    RNA_INPUT_SOURCE_TYPES = ["input", "fasta"]
    def __int__(self):
        self.output = ""

    def execute(self, datapoint):
        self.output = ViennaRNA.fold(datapoint.sequence)

    def get_ss_prediction(self):
        if self.output == "":
            raise RNAFoldExecutionException(f"RNAFold exception: no output generated. Have you installed it?")
        ss = self.output[0]
        return ss

    def get_mfe(self):
        if self.output == "":
            raise RNAFoldExecutionException(f"RNAFold exception: no output generated. Have you installed it?")
        mfe = self.output[1]
        return mfe

class RNAFoldExecutionException(Exception): pass
