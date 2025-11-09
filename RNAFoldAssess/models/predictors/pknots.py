import os

from RNAFoldAssess.utils.secondary_structure_tools import SecondaryStructureTools


class PKnots:
    def __init__(self, ct_dir):
        self.output = ""
        self.ct_dir = ct_dir
        self.output_subfolder = ""

    def execute(self, fasta_file, output_subfolder="", path="", remove_file_when_done=False):
        self.output_subfolder = output_subfolder
        if path == "":
            path = "/mnt/nrdstor/yesselmanlab/ewhiting/pknots_v1.2/bin/pknots"

        if "/.ct" in fasta_file:
            fasta_file = fasta_file.replace("/.ct", ".ct")
        short_fasta_name = fasta_file.split("/")[-1]
        if output_subfolder == "":
            ct_path = f"{self.output_dir}/{short_fasta_name}.ct"
        else:
            ct_path = f"{self.ct_dir}/{output_subfolder}/{short_fasta_name}.ct"
        exec_string = f"{path} -g {fasta_file} {ct_path}"
        os.system(exec_string)
        self.output = SecondaryStructureTools.ct2db(ct_path)


    def get_ss_prediction(self):
        if self.output == "":
            raise Exception(f"PKnots exception: no output generated")
        return self.output