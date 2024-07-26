import os

from RNAFoldAssess.utils.secondary_structure_tools import SecondaryStructureTools


class PKnots:
    def __init__(self):
        self.output = ""
        self.output_subfolder = ""
        self.ct_dir = "/work/yesselmanlab/ewhiting/pknot_outputs"

    def execute(self, fasta_file, output_subfolder, path="", remove_file_when_done=False):
        self.output_subfolder = output_subfolder
        if path == "":
            path = "/common/yesselmanlab/ewhiting/pknots_v1.2/bin/pknots"

        if "/.ct" in fasta_file:
            fasta_file = fasta_file.replace("/.ct", ".ct")
        ct_path = f"{self.ct_dir}/{output_subfolder}/{fasta_file}.ct"
        exec_string = f"{path} -g {fasta_file} {ct_path}"
        os.system(exec_string)
        self.output = SecondaryStructureTools.ct2db(ct_path)
        if self.output != "":
            try:
                os.remove(ct_path)
            except Exception:
                print(f"PKnots couldn't remove {ct_path}")


    def get_ss_prediction(self):
        if self.output == "":
            raise Exception(f"PKnots exception: no output generated")
        return self.output
