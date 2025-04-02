import os


class ContextFold:
    def __init__(self):
        self.output = ""

    def execute(self, cf_path, sequence):
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