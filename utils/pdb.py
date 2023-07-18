import os


class PDB:
    """
    Utility class for getting PDB files
    """
    @staticmethod
    def get_file(rna_id):
        url = f"https://files.rcsb.org/download/{rna_id}.pdb"
        cmd = f"wget {url}"
        os.popen(cmd)
        pdb_file_path = os.path.abspath(f"{rna_id}.pdb")
        return pdb_file_path

