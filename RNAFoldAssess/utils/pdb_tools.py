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
        # temp testing
        # row = '"NR_4.0_12763.26","7QI4|1|A","7QI4|1|A,7OF0|1|A,6ZM6|1|A,7QI5|1|A,7O9M|1|A,7OF6|1|A,8OIT|1|B8,7OF4|1|A,6ZM5|1|A,7OF7|1|A,7QI6|1|A,6VMI|1|A,6VLZ|1|A,7OF2|1|A,8OIR|1|B8,7OF3|1|A,7L20|1|A,7ODR|1|A,7A5J|1|A,7OF5|1|A,7ODT|1|A,7O9K|1|A,5OOL|1|A,7ODS|1|A,7OIC|1|A,7A5H|1|A,7L08|1|A,7PO4|1|A,7QH7|1|A,7OIE|1|A,6ZSC|1|XA,7A5K|1|A3,7A5I|1|A3,7OID|1|A,6ZSD|1|XA,7PD3|1|A,7OG4|1|XA,7QH6|1|A,3J9M|1|A,6I9R|1|A,5OOM|1|A,6ZSG|1|XA,6ZSA|1|XA,6ZS9|1|XA,7OIA|1|A,3J7Y|1|A,7OIB|1|A,7OI9|1|A,6NU2|1|A,7OI8|1|A,7OI7|1|A"'
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

