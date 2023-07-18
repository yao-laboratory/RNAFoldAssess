import subprocess, os


dssr_path = "/home/yesselmanlab/ewhiting/x3dna/bin/x3dna-dssr"
dbn_path = ""

class DSSR:
    """
    A class for easily calling DSSR. All methods are static.
    If you're using this in your own environment, please
    update the path variables above to match your path
    """
    @staticmethod
    def get_ss_from_pdb(path_to_pdb):
        file_extension = path_to_pdb.split(".")[-1]
        if file_extension != "pdb":
            raise Exception("File must be pdb type")
        # Run X3DNA-DSSR
        cmd_string = f"{dssr_path} -i={path_to_pdb}"
        process = subprocess.Popen(
            cmd_string.split(), None, stdout=subprocess.PIPE
        )
        _output, error = process.communicate()
        if error:
            raise Exception("Error running DSSR")
        # Get the ss output string
        f = data = open("dssr-2ndstrs.dbn")
        data = f.read()
        f.close()
        # Remove generated files that we don't need
        os.popen("rm dssr-*")
        return data
