class DataPoint2:
    CHEMICAL_MAPPING_TYPES = ["DMS", "SHAPE", "CMCT"]

    def __init__(self, name, sequence, ground_truth_type=None, ground_truth_data=None, cohort=None, reads=None):
        self.name = name
        self.sequence = sequence
        self.ground_truth_type = ground_truth_type
        self.ground_truth_data = ground_truth_data
        self.cohort = cohort
        self.reads = reads


    def to_seq_file(self, path=None):
        file_name = f"{self.name}.seq"
        if path:
            file_name = f"{path}/{file_name}"

        sequence_grouping = 8
        line_grouping = 4

        fstring = ""
        counter = 0
        for i in range(0, len(self.sequence), sequence_grouping):
            counter += 1
            if counter == line_grouping:
                counter = 0
                trailing = "\n"
            else:
                trailing = " "
            fstring += self.sequence[i:i+8] + trailing

        with open(file_name, "w") as fh:
            fh.write(fstring.strip())

        return file_name

    def to_fasta_file(self, path=None):
        file_name = f"{self.name}.fasta"
        if path:
            file_name = f"{path}/{file_name}"

        fstring = f">{self.name}\n{self.sequence}"

        with open(file_name, "w") as fh:
            fh.write(fstring)

        return file_name

    def to_dbn_file(self, path=None, dbn=None):
        if self.ground_truth_type != "dbn" and not dbn:
            raise Exception(f"Cannot write .dbn file for {self.name}: no dbn given")

        if not dbn:
            dbn = self.ground_truth_data

        file_name = f"{self.name}.dbn"
        if path:
            file_name = f"{path}/{file_name}"

        fstring = f">{self.name}\n{self.sequence}\n{dbn}"

        with open(file_name, "w") as fh:
            fh.write(fstring)

        return file_name

    def to_constraint_file(self, path=None, reactivities=None):
        if self.ground_truth_data not in self.CHEMICAL_MAPPING_TYPES and not reactivities:
            raise Exception(f"Cannot write constraint file for {self.name}: no reactivities given")

        if not reactivities:
            reactivities = self.ground_truth_data

        file_name = f"{self.name}.cf"
        if path:
            file_name = f"{path}/{file_name}"

        is_dms = self.ground_truth_type == "DMS"
        is_cmct = self.ground_truth_type = "CMCT"

        if is_dms:
            non_reactants = ["G", "T", "U"]
        elif is_cmct:
            non_reactants = ["A", "C", "G"]
        else:
            # Otherwise, it's SHAPE
            non_reactants = []

        fstring = ""
        for i in range(len(reactivities)):
            mu = str(reactivities[i])
            if self.sequence[i] in non_reactants:
                mu = "-999"
            fstring += str(i + 1) + "\t" + mu + "\n"

        with open(file_name, "w") as fh:
            fh.write(fstring)

        return file_name

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
