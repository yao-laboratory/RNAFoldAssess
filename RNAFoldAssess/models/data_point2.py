class DataPoint2:
    def __init__(self, name, sequence, ground_truth_type=None, ground_truth_data=None, cohort=None, reads=None):
        self.name = name
        self.sequence = sequence
        self.ground_truth_type = ground_truth_type
        self.ground_truth_data = ground_truth_data
        self.cohort = cohort
        self.reads = reads


    # Initialization methods
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
        data = DataPoint2.extract_data_from_file(path_to_fasta)

        name = data[0].replace(">", "")
        seq = data[1]
        dp = DataPoint2(name, seq, cohort=cohort)
        return dp

    @staticmethod
    def init_from_dbn_file(path_to_dbn, cohort=None):
        data = DataPoint2.extract_data_from_file(path_to_dbn)
        name_line = data[0]
        name = name_line.replace(">", "").replace(" ", "_")
        seq = data[1]
        dbn = data[2]
        dp = DataPoint2(name, seq, cohort=cohort, ground_truth_type="dbn", ground_truth_data=dbn)
        return dp


    @staticmethod
    def init_from_seq_file(path_to_seq, cohort=None):
        data = DataPoint2.extract_data_from_file(path_to_seq)
        title_line = data.pop(0)
        name = title_line.replace(" ", "_")
        if title_line[-1].endswith(" 1"):
            title_line[-1] = title_line[-1].replace(" 1", "")
        seq = ""
        for sequence_line in data:
            seq += "".join(sequence_line)

        dp = DataPoint2(name, seq, cohort=cohort)
        return dp


    @staticmethod
    def extract_data_from_file(file_path):
        with open(file_path) as fh:
            data = [line.strip() for line in fh.readlines()]
        relevant_lines = []
        for d in data:
            if not d.startswith(";"):
                relevant_lines.append(d)

        return relevant_lines
