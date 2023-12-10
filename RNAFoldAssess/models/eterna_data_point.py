import os, json, heapq

from RNAFoldAssess.models.scorers import DSCI


class EternaDataPoint:
    def __init__(self, data_hash, normalize_reactivities_on_init=True):
        self.name = data_hash["name"]
        self.sequence = data_hash["sequence"]
        self.mapping_method = data_hash["mapping_method"]
        self.positions = data_hash["positions"]
        self.reactivities = data_hash["reactivities"]
        self.unnegate_negatives()
        if normalize_reactivities_on_init:
            self.normalize_reactivities()

    def unnegate_negatives(self):
        for i, r in enumerate(self.reactivities):
            if r <= 0:
                self.reactivities[i] = 0

    def normalize_reactivities(self):
        largest = heapq.nlargest(1, self.reactivities)[0]
        if largest > 0:
            for i, r in enumerate(self.reactivities):
                new_val = round(r / largest, 6)
                self.reactivities[i] = new_val

    def to_seq_file(self):
        f = open(f"{name}.seq", "w")
        f.write(self.sequence)
        f.close()
        self.seq_path = os.path.abspath(f"{name}.seq")
        return self.seq_path

    def to_fasta_file(self):
        data = f">{name}\n{self.sequence}"
        f = open(f"{name}.fasta", "w")
        f.write(data)
        f.close()
        self.fasta_path = os.path.abspath(f"{name}.fasta")
        return self.fasta_path

    # We have to implement DSCI in a special way with these data points
    # becase there isn't reactivity for every data point
    def assess_prediction(self, ss_prediction):
        structure = ""
        reactivities = []
        sequence = ""
        for pos in self.positions:
            structure += ss_prediction[pos]
            sequence += self.sequence[pos]
            reactivities.append(self.reactivities[pos])

        DMS = False
        SHAPE = False
        if self.mapping_method == "SHAPE":
            SHAPE = True
        if self.mapping_method == "DMS":
            DMS = True

        return DSCI.score(
            sequence=sequence,
            secondary_structure=structure,
            reactivities=reactivities,
            DMS=DMS,
            SHAPE=SHAPE
        )


    @staticmethod
    def factory(path):
        f = open(path)
        json_data = json.loads(f.read())
        f.close()
        data_points = []
        for datum in json_data:
            data_points.append(EternaDataPoint(datum))
        return data_points

