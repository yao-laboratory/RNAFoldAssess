import os, json, heapq


class DataPoint:
    """
    The `DataPoint` class was developped while working with DMS data in our lab. The
    data we had was captured in a JSON file and looked something like the following:

    ```json
    [
        {
            "name": "sequence_1",
            "sequence": "ACGUG",
            "structure": ".....",
            "data": [0.8, 0.9, 0.7, 0.7, 0.6],
            "reads": 312
        },
        {
            "name": "sequence_2",
            ... etc ...
        }
    ]
    ```

    Each file contained thousands of data points, and data points across files had
    similar names. Therefore, we used the file name as a "cohort." So, if we had
    two files of 100 squences each called DMS_FILE_1.json and DMS_FILE_2.json, then
    sequence_1 from the first file was in chort DMS_FILE_1 and its name was
    DMS_FILE_1_sequence_1. Likewise, in the DMS_FILE_2.json file, the data point named
    sequence_1 was called DMS_FILE_2_sequence_1.

    If you wish to use this class, the constructor needs, at least, a `data_hash` value
    that is a dictionary and has at least a name, sequence, and data attribute. The
    reads attribute is optional.

    Similarly, if you have a JSON file with several data points in them, you can use
    this class's static `factory` method to create a list of those data points:

    ```python
    from RNAFoldAssess.models import DataPoint

    dms_file_loc = "data/experiment_1.json"
    data_points = DataPoint.factory(dms_file_loc)
    ```

    Please note, the JSON data in the file must have at least a name, sequence, and
    data attribute.
    """
    def __init__(self, data_hash, cohort=None, normalize_reactivities_on_init=False, normalize_and_unnegate_reactivities_on_init=False):
        self.name = data_hash["name"]
        if cohort:
            self.name = f"{cohort}_{self.name}"
        self.sequence = data_hash["sequence"]
        self.reactivities = data_hash["data"]
        self.reads = data_hash["reads"] if "reads" in data_hash else None
        self.cohort = cohort
        if normalize_and_unnegate_reactivities_on_init:
            normalize_reactivities_on_init = True
            self.__unnegate_reactivities()
        if normalize_reactivities_on_init:
            self.__normalize_reactivities()

    def to_seq_file(self):
        # Make the name safe to be a filename
        file_safe_name = "".join(c for c in self.name if c.isalnum())
        if len(file_safe_name) > 200:
            file_safe_name = file_safe_name[0:200]
        f = open(f"{file_safe_name}.seq", "w")
        f.write(self.sequence)
        f.close()
        self.path = os.path.abspath(f"{file_safe_name}.seq")
        return self.path

    def to_fasta_file(self):
        # Make the name safe to be a filename
        file_safe_name = "".join(c for c in self.name if c.isalnum())
        if len(file_safe_name) > 200:
            file_safe_name = file_safe_name[0:200]
        data = f">{file_safe_name}\n{self.sequence}"
        f = open(f"{file_safe_name}.fasta", "w")
        f.write(data)
        f.close()
        self.path = os.path.abspath(f"{file_safe_name}.fasta")
        return self.path

    def to_fasta_string(self):
        return f">{self.name} en=0.00\n{self.sequence}\n"

    def to_constraint_file(self, destination_dir=None):
        # Make the name safe to be a filename
        file_safe_name = "".join(c for c in self.name if c.isalnum())
        if len(file_safe_name) > 200:
            file_safe_name = file_safe_name[0:200]
        file_name = f"{file_safe_name}_struc_constraint.txt"
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
    def get_structure_probabilities(path):
        """
        This method will take a file containing a json array of DMS data and
        create a consensus structure from the sequences. This method assumes
        that all sequences in the json file are the same length. The object
        returned from this method is a dictionary containing two keys:

            consensus: the consensus structure
            probabilities: each RNA nucleotide (A, C, G, U) and its probability
                           from 0 to 1 of being at that location in the sequence
        """
        f = open(path)
        json_data = json.loads(f.read())
        f.close()
        sequence_scores = []
        sequence_length = len(json_data[0]["sequence"])
        for i in range(sequence_length):
            sequence_scores.append({
                "A": [0, 0.0],
                "C": [0, 0.0],
                "U": [0, 0.0],
                "G": [0, 0.0]
            })
        for datum in json_data:
            seq = datum["sequence"]
            for i in range(sequence_length):
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
    def combined_structure_probabilities(paths):
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
        # Using a simple normalizer
        largest = max(self.reactivities)
        if largest > 0:
            for i, r in enumerate(self.reactivities):
                new_val = round(r / largest, 6)
                self.reactivities[i] = new_val

    def __unnegate_reactivities(self):
        for i, r in enumerate(self.reactivities):
            if r < 0:
                self.reactivities[i] = 0.0
