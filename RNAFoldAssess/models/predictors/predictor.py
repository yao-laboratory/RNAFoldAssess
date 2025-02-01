class Predictor:
    """
    """

    def __init__(self):
        """
        We raise an exception when we try to use `get_ss_prediction`
        or `get_mfe` before running `execute`. To make that happen,
        we check for a blank `output` attribute, which we set here.

        Some other inputs that may be useful here are a path to the
        prediction tool's executable. In some cases, prediction tools
        are available via Python package (for example, RNAFold is
        available via the ViennaRNA package). Other times, prediction
        tools are only available as command line tools. In that case,
        you may wnat to include a path to that command line tool's
        executable in the `__init__` parameters.
        """
        self.output = ""
    
    def execute(self):
        """
        This method should encapsulate the requirments for running a
        tool's prediction algorithm given an RNA sequence, and
        returning setting the `output` attribute to contain the
        relevant data from the tool's output. In this method, you
        will likely always need to include a parameter representing an
        RNA sequence. Some tools can take a sequnce from STDIN, others
        may need a path to a .fasta, .seq, or other file. In either
        case, you will have to include that parameter in this method
        signature and write code to get the appropriate RNA data
        source to the prediction tool.

        As an example example, in the RNAFold model, the `execute`
        method requires a sequence source and source type. The source
        type indicates whether the RNA sequence is `input` (i.e., from
        STDIN) or a fasta file. Since RNAFold is provided via the
        ViennaRNA package, all we need is the sequence of nucleotides
        to get a prediction. So, if we are given a path to a fasta
        file, we open the file and extract the RNA sequence from it so
        we can pass it to the `ViennaRNA.fold` method.

        After running the tool, you will need to capture the tool's
        output somehow. If your tool is available via a Python package,
        you most likely don't have to do much here. If you have to
        call your tool frmo the command line via `os.system` or
        something like that, you will probably have to use some like
        `os.popen(<execution string>).read()` to read directly from
        STDOUT. Other tools will write their prediction to an output
        file, in that case, you will have to somehow associate that
        file (either its path or conetns) with the `output` attribute.

        For example, in the RNAFold model, after we get the tool's
        secondary structure prediction via the `fold` method, we set
        the `output` variable to be the return value of `fold`.
        """
        raise NotImplementedError
    
    def get_ss_prediction(self):
        """
        This method should include the logic for parsing the class's
        `output` attribute and returning a dot-bracket notation of
        the model's prediction. Some models return output to STDOUT,
        in which case you should have read that into this class's
        `output` variable. Other tools may write their prediction to
        a file; these predictions can sometimes be a raw .dbn string
        or a contact-table or .bpseq file. In either case, this method
        should parse the tool's output and return a dot-bracket
        notation string.

        This method should also check if the `output` attribute is
        a blank string and, if so, raise an exception. This is to
        ensure pipelines are remembering to `execute` the tools before
        trying to parse their output.

        As an example, the `execute` method for the RNAFold class
        returns a two-item list. The first item is a dot-brack string
        of the model's prediction, and the second item is the minimum
        free energy (MFE) of the prediction. In that case, in the
        `get_ss_prediction` method, we check that the output attribute
        isn't a blank string (and raise an exception if it is), then
        return the first item of the output attribute.
        """
        raise NotImplementedError
    
    def get_mfe(self):
        """
        This method, while not required, may be of use to some
        researchers. The code in this method should include the logic
        for retrieving the minimum free energy (MFE) from a tool's
        prediction. Not all tools return an MFE, in which case, you
        should not implement this method, unless you have another means
        of calculating that information and need to include it in your
        pipeline.

        As an example, the `execute` method for the RNAFold class
        returns a two-item list. The first item is a dot-brack string
        of the model's prediction, and the second item is the MFE
        of the prediction. In that case, in the `get_mfe` method, we
        check that the output attribute isn't a blank string (and raise
        an exception if it is), then return the second item of the
        output attribute.
        """
        raise NotImplementedError
