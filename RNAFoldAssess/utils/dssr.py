import os


dssr_path = "/home/yesselmanlab/ewhiting/x3dna/bin/x3dna-dssr"
dbn_path = ""

class DSSR:
    """
    A class for easily calling DSSR. All methods are static.
    If you're using this in your own environment, please
    update the path variables above to match your path
    """
    @staticmethod
    def get_ss_from_pdb(path_to_pdb, destination_dir="."):
        file_name = path_to_pdb.split("/")[-1]
        name, file_extension = file_name.split(".")
        if file_extension not in ["pdb", "cif"]:
            raise Exception("File must be pdb or cif type")
        # Run X3DNA-DSSR
        cmd_string = f"{dssr_path} -i={path_to_pdb}"
        try:
            os.system(cmd_string)
            # Get the ss output string
            f = open("dssr-2ndstrs.dbn")
            data = f.read()
            f.close()
            dbn_file = open(f"{destination_dir}/{name}.dbn", "w")
            dbn_file.write(data)
            dbn_file.close()
            # Remove generated files that we don't need
            os.system("rm dssr-*")
            return data
        except Exception as e:
            print(f"DSSR Exception: {e}")

