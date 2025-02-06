class DataPoint2:
    def __init__(self, name, sequence, ground_truth_type=None, ground_truth_data=None, cohort=None, reads=None):
        self.name = name
        self.sequence = sequence
        self.ground_truth_type = ground_truth_type
        self.ground_truth_data = ground_truth_data
        self.cohort = cohort
        self.reads = reads

    @staticmethod
    def init_from_dict(dict_object, name=None, cohort=None):
        if not name:
            name = list(dict_object.keys())[0]
        seq = dict_object.get("sequence", None)
        reads = dict_object.get("reads", None)
        reactivities = dict_object.get("data", None)
        dbn_string = dict_object.get("dbn", None)
        if reactivities:
            ground_truth_type = dict_object.get("experiment_type", "DMS") # default to DMS since it is the least harmful assumption
            ground_truth_data = reactivities
        elif dbn_string:
            ground_truth_type = "dbn"
            ground_truth_data = dbn_string

        dp = DataPoint2(name, seq, ground_truth_type, ground_truth_data, cohort, reads)
        return dp

    @staticmethod
    def init_from_fasta(path_to_fasta, cohort=None):
        with open(path_to_fasta) as fh:
            fasta_data = [line.strip() for line in fh.readline()]

        name = fasta_data[0]
        seq = fasta_data[1]
        dp = DataPoint2(name, seq)
        return dp
