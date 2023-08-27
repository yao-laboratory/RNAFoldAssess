import json
import os


class PDB:
    """
    Utility class for getting PDB files
    """
    @staticmethod
    def default_data_dir():
        return "/home/yesselmanlab/ewhiting/RNAFoldAssess/RNAFoldAssess/data"

    @staticmethod
    def get_file(rna_id, destination_dir=None):
        url = f"https://files.rcsb.org/download/{rna_id}.pdb"
        if not destination_dir:
            destination_dir = PDB.default_data_dir()
        destination_dir = os.path.abspath(destination_dir)
        cmd = f"wget -O {destination_dir}/{rna_id}.pdb {url}"
        os.system(cmd)
        pdb_file_path = os.path.abspath(f"{rna_id}.pdb")
        return pdb_file_path


    @staticmethod
    def download_files_from_json(input_file, destination_dir):
        input_file = os.path.abspath(input_file)
        f = open(input_file)
        raw_data = f.read()
        f.close()
        data = json.loads(raw_data)["result_set"]
        for d in data:
            PDB.get_file(d["identifier"], destination_dir)
