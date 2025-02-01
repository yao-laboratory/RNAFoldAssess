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
        2. Call the `execute` method, passing it an RNA sequence source and source type
            a. The acceptable source types are "input" for a raw string or
               "fasta" for a fasta file.
            b. The default source type is "input," so this class expects a raw string
               if you do not specify the input is a fasta file.
            c. If you set source type as fasta and the fasta file is not at the path
               you specified, this class will raise an `RNAFoldExecutionException`
        3. To get the secondary structure prediction after execution:
            a. Use the `get_ss_prediction` method. This will return a dot-brack
               notation (dbn) string of the prediction.
            b. If the `execute` method failed for some reason besides a missing file
               path. The `get_ss_prediction` method will raise an
               `RNAFoldExecutionException`
    """

    RNA_INPUT_SOURCE_TYPES = ["input", "fasta"]
    def __int__(self):
        self.output = ""

    def execute(self, rna_sequece_source, source_type="input"):
        rna_source_type = source_type.lower()
        if rna_source_type not in self.RNA_INPUT_SOURCE_TYPES:
            raise Exception(f"Source type for RNAFold must be in `{self.RNA_INPUT_SOURCE_TYPES}`. Not {source_type}")
        
        if rna_source_type == "input":
            sequence = rna_sequece_source
        elif rna_source_type == "fasta":
            try:
                with open(rna_sequece_source) as fh:
                    seq_data = [line.strip() for line in fh.readlines()]
            except FileNotFoundError:
                raise RNAFoldExecutionException(f"Could not find file at {rna_sequece_source}")
            sequence = seq_data[1]

        self.output = ViennaRNA.fold(sequence)


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

class RNAFoldExecutionException: pass
