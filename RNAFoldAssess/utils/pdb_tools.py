import json, os, re, requests, datetime


class PDBTools:
    """
    Utility class for getting PDB files
    """
    @staticmethod
    def default_data_dir():
        return "/home/yesselmanlab/ewhiting/RNAFoldAssess/RNAFoldAssess/data"

    @staticmethod
    def get_pdb_file(rna_id, destination_dir=None):
        url = f"https://files.rcsb.org/download/{rna_id}.pdb"
        if not destination_dir:
            destination_dir = PDBTools.default_data_dir()
        destination_dir = os.path.abspath(destination_dir)
        cmd = f"wget -O {destination_dir}/{rna_id}.pdb {url}"
        os.system(cmd)


    @staticmethod
    def get_mmcif_file(rna_id, destination_dir):
        url = f"https://files.rcsb.org/view/{rna_id}.cif"
        if not destination_dir:
            destination_dir = PDBTools.default_data_dir()
        destination_dir = os.path.abspath(destination_dir)
        cmd = f"wget -O {destination_dir}/{rna_id}.cif {url}"
        os.system(cmd)

    @staticmethod
    def download_files_from_json(input_file, destination_dir):
        input_file = os.path.abspath(input_file)
        f = open(input_file)
        raw_data = f.read()
        f.close()
        data = json.loads(raw_data)["result_set"]
        for d in data:
            PDBTools.get_file(d["identifier"], destination_dir)

    @staticmethod
    def get_molecule_from_ebi(pdb_id):
        url = f'https://www.ebi.ac.uk/pdbe/api/pdb/entry/molecules/{pdb_id}'
        data = requests.get(url).json()[pdb_id.lower()]
        return data


    @staticmethod
    def get_canonical_pdb_ids(input_file_path):
        latest_ids = []
        input_file = os.path.abspath(input_file_path)
        input_file = open(input_file)
        pdb_ids = input_file.readlines()
        input_file.close()
        for pdb_id in pdb_ids:
            if len(pdb_id) == 5:
                pdb_id = pdb_id.strip()
        master_file_path = "/common/yesselmanlab/ewhiting/data/canonical.csv"
        fp = open(master_file_path)
        canonical_lines = fp.readlines()
        fp.close()
        for pdb_id in pdb_ids:
            if len(pdb_id) >= 4:
                if len(pdb_id) == 5:
                    pdb_id = pdb_id.strip()
                latest_ids.append(
                    PDBTools._get_latest_pdb(canonical_lines, pdb_id)
                )
        # Remove duplicates
        latest_ids = set(latest_ids)
        print(f"Given PDBs: {len(pdb_ids)}")
        print(f"Latest PDBs: {len(latest_ids)}")
        return latest_ids

    @staticmethod
    def _get_latest_pdb(csv_lines, pdb_id):
        for row in csv_lines:
            data = row.split('"')
            for d in data:
                if d in ['', ","]:
                    data.remove(d)
            if data[1].split("|")[0] == pdb_id:
                print(f"getting {pdb_id}")
                other_ids = []
                dup_info = data[2]
                dup_info = re.split("\||\,|\+", dup_info)
                for item in dup_info:
                    if len(item) == 4:
                        other_ids.append(item)
                for id in other_ids:
                    if id == pdb_id:
                        other_ids.remove(id)
                latest_id = pdb_id
                latest_date = 0 # Will fil this out in just a moment
                cif = requests.get(f"https://files.rcsb.org/header/{pdb_id}.cif")
                lines = cif.iter_lines()
                for line in lines:
                    line = line.decode()
                    if "recvd_initial_deposition_date" in line:
                        dep_date = line.split()[-1]
                        latest_date = datetime.datetime.strptime(dep_date, "%Y-%m-%d")
                        continue
                for id in other_ids:
                    cif = requests.get(f"https://files.rcsb.org/header/{pdb_id}.cif")
                    lines = cif.iter_lines()
                    for line in lines:
                        line = line.decode()
                        if "recvd_initial_deposition_date" in line:
                            dep_date = line.split()[-1]
                            new_date = datetime.datetime.strptime(dep_date, "%Y-%m-%d")
                            if new_date > latest_date:
                                latest_date = new_date
                                latest_id = id
                            continue
                return latest_id

