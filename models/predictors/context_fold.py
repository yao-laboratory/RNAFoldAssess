import os


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
