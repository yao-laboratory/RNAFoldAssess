import os, json, heapq


class DataPoint:
    def __init__(self, data_hash, cohort=None, normalize_reactivities_on_init=False):
        self.name = data_hash["name"]
        if cohort:
            self.name = f"{cohort}_{self.name}"
        self.sequence = data_hash["sequence"]
        self.reactivities = data_hash["data"]
        self.reads = data_hash["reads"]
        self.cohort = cohort
        if normalize_reactivities_on_init:
            self.__normalize_reactivities()

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

    def to_fasta_string(self):
        return f">{self.name} en=0.00\n{self.sequence}\n"

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
    def write_large_fasta_file(path, cohort, name_suffix):
        file_name = f"{cohort}_{name_suffix}.fa"
        data_points = DataPoint.factory(path, cohort)
        f = open(file_name, "w")
        for dp in data_points:
            f.write(dp.to_fasta_string())
        f.close()

    @staticmethod
    def factory(path, name_prefix=None):
        f = open(path)
        json_data = json.loads(f.read())
        f.close()
        data_points = []
        for datum in json_data:
            data_points.append(DataPoint(datum, name_prefix))
        return data_points

    @staticmethod
    def get_structure_probabilities(path, name_prefix=None):
        f = open(path)
        json_data = json.loads(f.read())
        f.close()
        sequence_scores = []
        for i in range(65):
            sequence_scores.append({
                "A": [0, 0.0],
                "C": [0, 0.0],
                "U": [0, 0.0],
                "G": [0, 0.0]
            })
        for datum in json_data:
            seq = datum["sequence"]
            for i in range(65):
                nt = seq[i]
                sequence_scores[i][nt][0] += 1
        for score in sequence_scores:
            for nt in score:
                score[nt][1] = round(score[nt][0] / len(json_data), 2)
        consensus_sequence = ""
        for score in sequence_scores:
            consensus_sequence += max(score, key=score.get)
        return { "consensus": consensus_sequence, "probabilities": sequence_scores }


    @staticmethod
    def combined_structure_probabilities(paths, name_prefixes=[]):
        data = []
        for path in paths:
            f = open(path)
            data.append(json.loads(f.read()))
            f.close()
        flattened_data = []
        for item in data:
            for datum in item:
                flattened_data.append(datum)
        del(data)
        sequence_scores = []
        for i in range(65):
            sequence_scores.append({
                "A": [0, 0.0],
                "C": [0, 0.0],
                "U": [0, 0.0],
                "G": [0, 0.0]
            })
        for datum in flattened_data:
            seq = datum["sequence"]
            for i in range(65):
                nt = seq[i]
                sequence_scores[i][nt][0] += 1
        for score in sequence_scores:
            for nt in score:
                score[nt][1] = round(score[nt][0] / len(flattened_data), 2)
        consensus_sequence = ""
        for score in sequence_scores:
            consensus_sequence += max(score, key=score.get)
        return { "consensus": consensus_sequence, "probabilities": sequence_scores }

    def __normalize_reactivities(self):
        n = 10
        nlargest = heapq.nlargest(n, self.reactivities)
        normalizer = sum(nlargest) / len(nlargest)
        self.normalized_reactivities = []
        for reactivity in self.reactivities:
            norm_val = reactivity / normalizer
            if norm_val > 1.0:
                norm_val = 1.0
            self.normalized_reactivities.append(norm_val)
