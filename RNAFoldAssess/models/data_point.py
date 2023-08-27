import os
import json


class DataPoint:
    def __init__(self, data_hash):
        self.name = data_hash["name"]
        self.sequence = data_hash["sequence"]
        self.reactivities = data_hash["data"]
        self.reads = data_hash["reads"]

    def to_seq_file(self):
        # .seq files are required for EternaFold
        f = open(f"{self.name}.seq", "w")
        f.write(self.sequence)
        f.close()
        self.path = os.path.abspath(f"{self.name}.seq")
        return self.path

    def to_fasta_file(self):
        # .fasta files are required for SPOT-RNA
        data = f">{self.name}\n{self.sequence}"
        f = open(f"{self.name}.fasta", "w")
        f.write(data)
        f.close()
        self.path = os.path.abspath(f"{self.name}.fasta")
        return self.path

    def to_constraint_file(self, destination_dir=None):
        # For the RNA Structure folding algorithm
        file_name = f"{self.name}_struc_constraint.txt"
        if not destination_dir:
            destination_dir = "."
        file_path = f"{destination_dir}/{file_name}"
        f = open(file_path, "w")
        for i in range(len(self.reactivities)):
            mu = str(self.reactivities[i])
            if self.sequence[i] in ["T", "G"]:
                mu = "-999"
            f.write(str(i + 1) + "\t" + mu + "\n")
        f.close()
        return file_path

    def __str__(self):
        return f"{self.name}, {self.sequence}, {self.reactivities}"

    @staticmethod
    def factory(path):
        f = open(path)
        json_data = json.loads(f.read())
        f.close()
        data_points = []
        for datum in json_data:
            data_points.append(DataPoint(datum))
        return data_points
