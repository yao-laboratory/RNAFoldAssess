import os

class DataPointFromCrystal:
    def __init__(self, name, sequence, true_structure, pdb_id=None, experiment_type=None, predicted_structure=None):
        self.name = name
        self.sequence = sequence
        self.true_structure = true_structure
        self.pdb_id = pdb_id
        self.experiment_type = experiment_type
        self.predicted_structure = predicted_structure

    def to_seq_file(self):
        name = self.name.replace(" ", "_")
        f = open(f"{name}.seq", "w")
        f.write(self.sequence)
        f.close()
        self.path = os.path.abspath(f"{name}.seq")
        return self.path

    def to_fasta_file(self):
        name = self.name.replace(" ", "_")
        data = f">{name}\n{self.sequence}"
        f = open(f"{name}.fasta", "w")
        f.write(data)
        f.close()
        self.path = os.path.abspath(f"{name}.fasta")
        return self.path

    def to_fasta_string(self):
        return f">{self.name} en=0.00\n{self.sequence}\n"

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