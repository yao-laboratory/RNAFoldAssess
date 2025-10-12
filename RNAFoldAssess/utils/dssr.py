import os


# Replace with the path to your own x3dna-dssr binary
dssr_path = os.getenv("DSSR_PATH")

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
            with open("dssr-2ndstrs.dbn") as fh:
                data = fh.read()
            with open(f"{destination_dir}/{name}.dbn", "w") as dbn_file:
                dbn_file.write(data)
            # Remove generated files that we don't need
            os.system("rm dssr-*")
            return data
        except Exception as e:
            print(f"DSSR Exception: {e}")

