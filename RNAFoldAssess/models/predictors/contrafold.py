import os


class ContraFold:
    """
    This predictor model is provided as an example, but is capable of being
    used as well. In order to use the ContraFold predictor class, you must
    first install the ContraFold package. Installation instructions for this
    package can be foundat the following link:

        http://contra.stanford.edu/contrafold/download.html

    Once you have ContraFold installed, you will use the path to the package
    as input to the class's `execute` method. To make a prediction with the
    ContraFold class from a seq file, consider the following example code:

    ```python
    model = ContraFold()
    path_to_contrafold_package = os.path.abspath("/home/user/tools/ContraFold")
    seq_file_path = os.path.abspath("/home/user/data/some_rna_file.seq)

    model.execute(path_to_contrafold_package, seq_file_path)
    prediction = model.get_ss_prediction()
    ```

    Note that running `execute` sets the model's `output` attribute to the
    predicted secondary structure in dot-bracket notation. To retrieve that
    dot-bracket string, you have to run the `get_ss_prediction` method.
    """
    def __init__(self):
        self.output = ""

    def execute(self, contra_path, seq_file, remove_file_when_done=True):
        exec_string = f"{contra_path}/src/contrafold predict {seq_file}"
        self.output = os.popen(exec_string).read()
        if remove_file_when_done:
            try:
                os.remove(seq_file)
            except FileNotFoundError:
                print(f"ContraFold exception: Couldn't find {seq_file} to delete")

    def get_ss_prediction(self):
        if self.output == "":
            raise Exception(f"ContraFold exception: no output generated")
        strings = self.output.split("\n")
        ss = strings[strings.index('>structure') + 1]
        return ss
