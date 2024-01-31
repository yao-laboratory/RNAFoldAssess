import os


class DataPointFromCrystal:
    """
    This class was created while we were working with output from PDB files,
    however, it is mostly a data point that is built via manual entry. The
    true_structure attribute can be extracted from the PDB file; we used x3dna
    in our work to get the "known" secondary structure. You can use whatever
    tool you want, but the structure should be in dot-bracket notation. This
    class doesn't provide any convenience methods like a secondary structure
    extractor, a sequence extractor, or even a means of downloading the PDB
    file remotely. The class assumes you already have sequence and secondary
    structure data.

    The static `factory` method in this class will create a list of data points
    if you give it a text file structured like so:

    ```
    >pdb_id_1 other=info
    ACGUGCUGUCGGU
    .(.....).....
    >pdb_id_2 other=info
    AGGUGCUGUCGGU
    .(.......)...
    ```
    """
    def __init__(self,
                 name,
                 sequence,
                 true_structure,
                 pdb_id=None,
                 experiment_type=None,
                 predicted_structure=None,
                 capitalize_sequence=True):
        self.name = name
        self.sequence = sequence.upper() if capitalize_sequence else sequence
        self.true_structure = true_structure
        self.pdb_id = pdb_id
        self.experiment_type = experiment_type
        self.predicted_structure = predicted_structure

    def to_seq_file(self):
        # Make the name safe to be a filename
        file_safe_name = "".join(c for c in self.name if c.isalnum())
        f = open(f"{file_safe_name}.seq", "w")
        f.write(self.sequence)
        f.close()
        self.path = os.path.abspath(f"{file_safe_name}.seq")
        return self.path

    def to_fasta_file(self):
        file_safe_name = "".join(c for c in self.name if c.isalnum())
        data = f">{file_safe_name}\n{self.sequence}"
        f = open(f"{file_safe_name}.fasta", "w")
        f.write(data)
        f.close()
        self.path = os.path.abspath(f"{file_safe_name}.fasta")
        return self.path

    def to_fasta_string(self, capitalize_sequence=True):
        sequence = self.sequence
        if capitalize_sequence:
            sequence = self.sequence.upper()
        return f">{self.name} en=0.00\n{sequence}\n"

    def get_experiment_type(self, pdb_id=None):
        if not self.pdb_id:
            self.pdb_id = pdb_id
        if not self.pdb_id:
            raise Exception("Cannot get experiment type without PDB ID. Please supply one to this method or set the object's `pdb_id` attribute.")
        # https://files.rcsb.org/header/{self.pdb_id}.pdb
        pdb_header = os.popen(f"curl https://files.rcsb.org/header/{self.pdb_id}.pdb").read()
        spl = pdb_header.split()
        for i, item in enumerate(spl):
            if item == "EXPDTA":
                self.experiment_type = spl[i+1]
                return self.experiment_type

    @staticmethod
    def factory(path):
        f = open(path)
        data = f.readlines()
        f.close()
        data_points = []
        for i in range(0, len(data), 3):
            name = data[i].strip().replace(">", "")
            seq = data[i+1].strip()
            true_structure = data[i+2].strip()
            pdb_id = name.split()[0]
            data_points.append(
                DataPointFromCrystal(
                    name=name,
                    sequence=seq,
                    true_structure=true_structure,
                    pdb_id=pdb_id
                )
            )
        return data_points

    @staticmethod
    def factory_from_dbn_files(path):
        dbn_files = [dbn for dbn in os.listdir(path) if dbn.endswith(".dbn")]
        data_points = []
        for dbn_file in dbn_files:
            f = open(f"{path}/{dbn_file}")
            lines = f.readlines()
            f.close()
            name = dbn_file.split(".")[0]
            seq = lines[1]
            true_structure = lines[2]
            data_points.append(
                DataPointFromCrystal(
                    name=name,
                    sequence=seq.strip(),
                    true_structure=true_structure.strip(),
                    pdb_id=name[:4]
                )
            )
        return data_points
