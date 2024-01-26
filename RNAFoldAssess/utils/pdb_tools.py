import os, requests


class PDBTools:
    """
    Utility class for getting PDB files
    """
    @staticmethod
    def get_pdb_file(rna_id, destination_dir):
        url = f"https://files.rcsb.org/download/{rna_id}.pdb"
        destination_dir = os.path.abspath(destination_dir)
        cmd = f"wget -O {destination_dir}/{rna_id}.pdb {url}"
        os.system(cmd)


    @staticmethod
    def get_mmcif_file(rna_id, destination_dir):
        url = f"https://files.rcsb.org/view/{rna_id}.cif"
        destination_dir = os.path.abspath(destination_dir)
        cmd = f"wget -O {destination_dir}/{rna_id}.cif {url}"
        os.system(cmd)


    @staticmethod
    def get_molecule_from_ebi(pdb_id):
        url = f'https://www.ebi.ac.uk/pdbe/api/pdb/entry/molecules/{pdb_id}'
        data = requests.get(url).json()[pdb_id.lower()]
        return data
