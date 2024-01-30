import os, json, heapq

from RNAFoldAssess.models.scorers import DSCI


class EternaDataPoint:
    """
    This class provides some utitliy functions for working with data from .rdat files
    in the EternaBench dataset. Specifically, the author of this repository worked with
    a lot of the files at this link:

    https://github.com/eternagame/EternaBench/tree/master/data/ChemMappingPreprocessing/raw_rdats

    and many of these methods are helper functions to handle that data.
    """
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
        """
        A lot of the chemical mapping data in the EternaBench dataset is
        negative, which will mess up the DSCI scoring algorithm. This
        method sets any negative number in the reactivity data to 0.
        """
        for i, r in enumerate(self.reactivities):
            if r <= 0:
                self.reactivities[i] = 0

    def normalize_reactivities(self):
        largest = max(self.reactivities)
        if largest > 0:
            for i, r in enumerate(self.reactivities):
                new_val = round(r / largest, 6)
                self.reactivities[i] = new_val

    def to_seq_file(self):
        # Make the name safe to be a filename
        file_safe_name = "".join(c for c in self.name if c.isalnum())
        f = open(f"{file_safe_name}.seq", "w")
        f.write(self.sequence)
        f.close()
        self.seq_path = os.path.abspath(f"{file_safe_name}.seq")
        return self.seq_path

    def to_fasta_file(self):
        # Make the name safe to be a filename
        file_safe_name = "".join(c for c in self.name if c.isalnum())
        data = f">{file_safe_name}\n{self.sequence}"
        f = open(f"{file_safe_name}.fasta", "w")
        f.write(data)
        f.close()
        self.fasta_path = os.path.abspath(f"{file_safe_name}.fasta")
        return self.fasta_path

    # We have to implement DSCI in a special way with these data points
    # becase there isn't reactivity for every data point
    def assess_prediction(self, ss_prediction):
        """
        We don't directly use the built-in DSCI scorer of RNAFoldAssess for
        EternaBench data because not every nucleotide in their dataset has
        reactivity data. As such, we don't count those nucleotides in the
        scoring of secondary structure predictions. We decide that there is
        "no reactivity data" if the reactivity data for that index is 0 (or
        negative implicitly since we unnegate all the reactivity data by default).
        """
        structure = ""
        sequence = ""
        for pos in self.positions:
            try:
                structure += ss_prediction[pos]
                sequence += self.sequence[pos]
            except Exception as e:
                print(f"Out of bounds error in {self.name}")

        DMS = False
        SHAPE = False
        if self.mapping_method == "SHAPE":
            SHAPE = True
        if self.mapping_method == "DMS":
            DMS = True

        return DSCI.score(
            sequence=sequence,
            secondary_structure=structure,
            reactivities=self.reactivities,
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
            # Some ad-hoc cleaning of the data
            dp = EternaDataPoint(datum)
            if dp.name.startswith("ETERNA_R73_0000_ANNOTATION"):
                dp.mapping_method = "SHAPE"
            if dp.name.startswith("ETERNA_R70_0000_ANNOTATION") and dp.mapping_method == "UNKNOWN":
                dp.mapping_method = "SHAPE"
            data_points.append(dp)
        return data_points

