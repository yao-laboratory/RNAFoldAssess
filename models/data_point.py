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

    @staticmethod
    def factory(path):
        f = open(path)
        json_data = json.loads(f.read())
        f.close()
        data_points = []
        for datum in json_data:
            data_points.append(DataPoint(datum))
        return data_points
