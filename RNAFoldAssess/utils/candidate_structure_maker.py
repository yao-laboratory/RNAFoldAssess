import os


from RNAFoldAssess.models.scorers import DSCI

## TODO

class CandidateStructureMaker:
    def __init__(self, name, sequence, reactivities, candidate_limit=1000, path_to_structure_file=""):
        self.datapoint_name = name
        self.datapoint_sequence = sequence
        self.datapoint_reactivities = reactivities
        self.candidate_structures = []
        self.candidate_limit = candidate_limit
        self.path_to_viennarna = path_to_viennarna

    def generate_structures(self):





