import os


class MXFold:
    def __int__(self):
        self.output = ""

    def execute(self, path, fasta_file, remove_file_when_done=True):
        path_to_mx_fold = os.path.abspath(path)
        exec_string = f"{path} {fasta_file}"
        self.output = os.popen(exec_string).read()
        if remove_file_when_done:
            print(f"MXFold object is deleting {fasta_file}")
            os.remove(fasta_file)

    def get_ss_prediction(self):
        if self.output == "":
            raise Exception(f"MXFold exception: no output generated")
        strings = self.output.split("\n")
        ss = strings[3]
        return ss
