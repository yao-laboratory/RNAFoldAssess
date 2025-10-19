import logging
import math, json, os, csv

from pathlib import Path
from typing import Union

from RNAFoldAssess.models.scorers import DSCI, BasePairScorer
from RNAFoldAssess.utils.sequence_tools import SequenceTools
from RNAFoldAssess.utils.normalizers import Normalizers

class DataPoint:
    CHEMICAL_MAPPING_TYPES = ["DMS", "dms", "SHAPE", "shape", "CMCT", "cmct"]
    ACCEPTABLE_GROUND_TRUTH_TYPES = CHEMICAL_MAPPING_TYPES + ["DBN", "dbn", "NONE"]

    def __init__(self, name, sequence, ground_truth_type=None, ground_truth_data=None, cohort=None, reads=None):
        self.name = name
        self.sequence = sequence
        self._ground_truth_type = None
        self.ground_truth_type = ground_truth_type
        self._ground_truth_data = None
        self.ground_truth_data = ground_truth_data
        self.cohort = cohort
        if cohort:
            self.name = f"{cohort}_{name}"
        self.reads = reads

    @property
    def ground_truth_type(self):
        return self._ground_truth_type

    @ground_truth_type.setter
    def ground_truth_type(self, gt_type):
        if gt_type is None:
            self._ground_truth_type = None
            return
        given_type = str(gt_type).upper()
        if given_type not in DataPoint.ACCEPTABLE_GROUND_TRUTH_TYPES:
            raise ValueError(
                f"The ground-truth type {gt_type} is not acceptable, "
                f"must be one of {DataPoint.ACCEPTABLE_GROUND_TRUTH_TYPES}"
            )
        self._ground_truth_type = given_type

    @property
    def ground_truth_data(self):
        return self._ground_truth_data

    @ground_truth_data.setter
    def ground_truth_data(self, gt_data):
        if self.ground_truth_type not in DataPoint.CHEMICAL_MAPPING_TYPES:
            self._ground_truth_data = gt_data
        else:
            if type(gt_data) == list:
                if len(gt_data) == len(self.sequence):
                    new_gt_data = {}
                    for i in range(len(self.sequence)):
                        new_gt_data[i] = gt_data[i]
                    self._ground_truth_data = new_gt_data
                else:
                    err_msg = f"DataPoint cannot accept list of reactivities unless list " \
                              f"is of equal size to sequence length. Please use a reactivity " \
                              f"map or use list equal in size to datapoint sequence.\n" \
                              f"DataPoint: {self.name}\nSequence: {self.sequence}\nProvided reactivities: {gt_data}"
                    raise Exception(err_msg)
            elif type(gt_data) == dict:
                positions = list(gt_data.keys())
                seq_len = len(self.sequence)
                for p in positions:
                    if int(p) > seq_len:
                        err_msg = f"Reactivitiy map is out of range. Encountered position {p} for " \
                                  f"sequence of length {seq_len}.\nSequence: {self.sequence}\n" \
                                  f"Positions: {positions}\nDatapoint: {self.name}\n" \
                                  f"Note that DataPoint expects 0-indexed reactivities"
                        raise Exception(err_msg)
                    elif int(p) < 0:
                        err_msg = f"Provided a negative position for reactivity map ({p}). " \
                                   "Please provide a zero-indexed reactivity map"
                        raise Exception(err_msg)
                new_gt_data = {}
                for p in positions:
                    new_gt_data[int(p)] = gt_data[p]
                self._ground_truth_data = new_gt_data

    @property
    def reactivities(self):
        if self.ground_truth_data is not None and self.ground_truth_type in DataPoint.CHEMICAL_MAPPING_TYPES:
            return list(self.ground_truth_data.values())
        else:
            raise Exception(f"Datapoint {self.name} does not have reactivities")

    @property
    def reactivity_map(self):
        if self.ground_truth_data is not None and self.ground_truth_type in DataPoint.CHEMICAL_MAPPING_TYPES:
            return self.ground_truth_data
        else:
            raise Exception(f"Datapoint {self.name} does not have reactivities")

    @property
    def structure(self):
        if self.ground_truth_type == "DBN":
            return self.ground_truth_data
        else:
            raise Exception(f"Datapoint {self.name} does not have a DBN string")

    def __eq__(self, other):
        name = self.name == other.name
        cohort = self.cohort == other.cohort
        seq = self.sequence == other.sequence
        gtd = self.ground_truth_data == other.ground_truth_data
        return name and cohort and seq and gtd

    # ---------------------------------------------------------------
    # Utility methods
    # ---------------------------------------------------------------

    def get_gc_content(self):
        return SequenceTools.get_gc_content(self.sequence)


    def get_sequence_entropy(self, log_base=4):
        return SequenceTools.get_sequence_entropy(self.sequence, log_base)

    def evaluate_prediction(self, prediction, lenience=0):
        if self.ground_truth_type == "DBN":
            return self.evaluate_prediction_with_known_dbn(prediction, lenience)
        else:
            return self.evaluate_prediction_with_mapping_data(prediction)

    def evaluate_prediction_with_known_dbn(self, prediction, lenience=0):
        if self.ground_truth_type != "DBN":
            raise Exception("Cannot evaluate datapoint without DBN ground-truth data")

        scorer = BasePairScorer(self.ground_truth_data, prediction, lenience)
        scorer.evaluate()
        return {
            "sensitivity": scorer.sensitivity,
            "PPV": scorer.ppv,
            "F1": scorer.f1
        }

    def evaluate_prediction_with_mapping_data(self, prediction):
        if self.ground_truth_type not in DataPoint.CHEMICAL_MAPPING_TYPES:
            raise Exception("DataPoint does not have reactivity data")

        reactivity_map = self.reactivity_map
        testable_reactivities = []
        testable_seq = ""
        testable_dbn = ""
        for pos, reactivity in reactivity_map.items():
            testable_reactivities.append(reactivity)
            testable_seq += self.sequence[pos]
            testable_dbn += prediction[pos]

        if self.ground_truth_type == "DMS":
            return DSCI.score(
                testable_seq,
                testable_dbn,
                testable_reactivities,
                DMS=True
            )
        elif self.ground_truth_type == "SHAPE":
            return DSCI.score(
                testable_seq,
                testable_dbn,
                testable_reactivities,
                SHAPE=True
            )
        elif self.ground_truth_type == "CMCT":
            return DSCI.score(
                testable_seq,
                testable_dbn,
                testable_reactivities,
                CMCT=True
            )
        else:
            raise Exception(f"RNAFoldAssess does not currently support scoring for {self.ground_truth_type} chemical mapping")

    def has_polyA_decreasing_reactivity(self, a_length=4):
        if self.ground_truth_type not in DataPoint.CHEMICAL_MAPPING_TYPES:
            logging.warning(f"You are chcking {self.name} for decreasing chemical probing reactivities, but {self.name} does not have chemical reactivity data. Returning False")
            return False
        decreasing_spans = Normalizers.detect_reactivity_dropoff_in_polyA(self.sequence, self.reactivity_map, a_length)
        return len(decreasing_spans) > 0


    # ---------------------------------------------------------------
    # File-writing methods
    # ---------------------------------------------------------------

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

    # def to_constraint_file(self, path=None, reactivities=None):
    #     TODO: Uncomment and fix problems here
    #     if self.ground_truth_data not in self.CHEMICAL_MAPPING_TYPES and not reactivities:
    #         raise Exception(f"Cannot write constraint file for {self.name}: no reactivities given")

    #     if not reactivities:
    #         reactivities = self.ground_truth_data

    #     file_name = f"{self.name}.cf"
    #     if path:
    #         file_name = f"{path}/{file_name}"

    #     is_dms = self.ground_truth_type == "DMS"
    #     is_cmct = self.ground_truth_type = "CMCT"

    #     if is_dms:
    #         non_reactants = ["G", "T", "U"]
    #     elif is_cmct:
    #         non_reactants = ["A", "C", "G"]
    #     else:
    #         # Otherwise, it's SHAPE
    #         non_reactants = []

    #     fstring = ""
    #     for i in range(len(reactivities)):
    #         mu = str(reactivities[i])
    #         if self.sequence[i] in non_reactants:
    #             mu = "-999"
    #         fstring += str(i + 1) + "\t" + mu + "\n"

    #     with open(file_name, "w") as fh:
    #         fh.write(fstring)

    #     return file_name

    def to_dictionary(self):
        obj = {
            "name": self.name,
            "sequence": self.sequence,
            "ground_truth_type": self.ground_truth_type
        }

        if self.ground_truth_type == "DBN":
            obj["dbn"] = self.structure
        else:
            obj["reactivity_map"] = self.ground_truth_data

        if self.cohort:
            name = self.name.replace(f"{self.cohort}_", "")
            obj["name"] = name
            obj["cohort"] = self.cohort

        if self.reads:
            obj["reads"] = self.reads

        return obj

    @staticmethod
    def to_csv_file(dp_list, path:Union[str, Path]="./datapoitns.csv"):
        headers = "name,sequence,ground_truth_type,ground_truth_data\n"
        lines = []
        for dp in dp_list:
            line = f"{dp.name},{dp.sequence},{dp.ground_truth_type},"
            if dp.ground_truth_type in DataPoint.CHEMICAL_MAPPING_TYPES:
                reactivity_map = dp.reactivity_map
                ground_truth_data = ";".join([f"{p}:{r}" for p, r in reactivity_map.items()])
            elif dp.ground_truth_type in ["DBN", "dbn"]:
                ground_truth_data = dp.ground_truth_data
            else:
                ground_truth_data = None
            line += f"{ground_truth_data}"
            lines.append(line)

        fstring = headers + "\n".join(lines)
        with open(path, "w") as fh:
            fh.write(fstring)

        return path


    @staticmethod
    def to_json_file(dp_list, path:Union[str, Path]="./datapoints.json"):
        dict_list = []
        for dp in dp_list:
            dict_list.append(dp.to_dictionary())

        with open(path, "w") as fh:
            json.dump(dict_list, fh)

        return path


    # ---------------------------------------------------------------
    # Initialization methods
    # ---------------------------------------------------------------

    @staticmethod
    def init_from_dict(dict_object, name=None, cohort=None):
        if not name:
            if "name" in dict_object.keys():
                name = dict_object["name"]
            else:
                name = list(dict_object.keys())[0]
                dict_object = dict_object[name]

        if "cohort" in dict_object.keys():
            cohort = dict_object["cohort"]

        seq = dict_object.get("sequence", None)
        reads = dict_object.get("reads", None)
        reactivities = dict_object.get("reactivity_map", None)
        if not reactivities:
            reactivities = dict_object.get("data", None)
        dbn_string = dict_object.get("dbn", None)
        if reactivities:
            ground_truth_type = dict_object.get("ground_truth_type", "DMS") # default to DMS since it is the least harmful assumption
            ground_truth_data = reactivities
        elif dbn_string:
            ground_truth_type = "DBN"
            ground_truth_data = dbn_string

        dp = DataPoint(name, seq, ground_truth_type, ground_truth_data, cohort, reads)
        return dp

    @staticmethod
    def init_from_fasta(path_to_fasta, cohort=None):
        data = DataPoint.extract_data_from_file(path_to_fasta)

        name = data[0].replace(">", "")
        if cohort:
            name = f"{cohort}_{name}"
        seq = data[1]
        dp = DataPoint(name, seq, cohort=cohort)
        return dp

    @staticmethod
    def init_from_dbn_file(path_to_dbn, cohort=None):
        data = DataPoint.extract_data_from_file(path_to_dbn)
        name_line = data[0]
        name = name_line.replace(">", "").replace(" ", "_")
        seq = data[1]
        dbn = data[2]
        dp = DataPoint(name, seq, cohort=cohort, ground_truth_type="DBN", ground_truth_data=dbn)
        return dp

    @staticmethod
    def init_from_dbn_files(directory_with_dbns, cohort=None):
        files = [f for f in os.listdir(directory_with_dbns) if f.endswith(".dbn")]

        if len(files) == 0:
            return []

        datapoints = []
        for f in files:
            path = f"{directory_with_dbns}/{f}"
            dp = DataPoint.init_from_dbn_file(path, cohort)
            datapoints.append(dp)

        return datapoints


    @staticmethod
    def init_from_seq_file(path_to_seq, cohort=None):
        data = DataPoint.extract_data_from_file(path_to_seq)
        title_line = data.pop(0)
        name = title_line.replace(" ", "_")
        if title_line[-1].endswith(" 1"):
            title_line[-1] = title_line[-1].replace(" 1", "")
        seq = ""
        for sequence_line in data:
            seq += "".join(sequence_line)

        dp = DataPoint(name, seq, cohort=cohort)
        return dp

    @staticmethod
    def factory_from_json(path, name_prefix=None):
        with open(path) as fh:
            json_data = json.load(fh)

        datapoints = []
        for datum in json_data:
            datapoints.append(DataPoint.init_from_dict(datum, cohort=name_prefix))

        return datapoints

    @staticmethod
    def init_from_rdat_file(path, cohort=None):
        name = path.split("/")[-1].replace(".rdat", "")
        with open(path) as fh:
            rdat_data = fh.readlines()

        # Find the first "ANNOTATION_DATA" entry
        annotation_data_line = ""
        for line in rdat_data:
            if line.startswith("ANNOTATION_DATA"):
                annotation_data_line = line
                break

        # The line is delimted by tabs
        annotation_data = annotation_data_line.split("\t")

        # The chemical type is in an item that starts with "modifier"
        # It's written as "modifier:type"
        for ad in annotation_data:
            if "modifier" in ad:
                experiment_type = ad.split(":")[1]
                break

        # The sequence is in an item that starts with "sequence"
        # It's written as "sequence:XXXX..XX"
        for ad in annotation_data:
            if "sequence" in ad:
                sequence = ad.split(":")[1].strip() # Remove \n character
                break

        # The positions for which the readings are available are annotated
        # in a line that starts with SEQPOS
        seqpos_line = ""
        for line in rdat_data:
            if line.startswith("SEQPOS"):
                seqpos_line = line
                break

        # SEQPOS annotates the positions in a 1-indexed list like this:
        # X1, X2, X3
        # We will split the line, remove the X's, and subtract 1 from the number
        positions = []
        for pos in seqpos_line.split("\t")[1:]: # Ignore the first item that is "SEQPOS"
            pos = pos.replace("X", "") # remove the X
            pos = int(pos) - 1
            positions.append(pos)

        # Now we get the first line of reactivities. Since we used ANNOTATION_DATA:1,
        # we will use the REACTIVITY:1 line.
        reactivity_line = ""
        for line in rdat_data:
            if line.startswith("REACTIVITY:1"):
                reactivity_line = line
                break

        # Reactivities are separated by tabs, we just need to make them into floats
        reactivities = []
        for r in reactivity_line.split("\t")[1:]:
            reactivities.append(float(r))

        reactivity_map = {}
        for i, p in enumerate(positions):
            reactivity_map[p] = reactivities[i]

        dp = DataPoint(
            name=name,
            sequence=sequence,
            ground_truth_type=experiment_type,
            ground_truth_data=reactivity_map,
            cohort=cohort
        )

        return dp

    @staticmethod
    def init_from_rdat_files(directory_with_rdats, cohort=None):
        files = [f for f in os.listdir(directory_with_rdats) if f.endswith(".rdat")]

        if len(files) == 0:
            return []

        datapoints = []
        for f in files:
            path = f"{directory_with_rdats}/{f}"
            dp = DataPoint.init_from_rdat_file(path, cohort)
            datapoints.append(dp)

        return datapoints

    @staticmethod
    def init_from_csv_file(csv_path:Union[str,Path], cohort=None):
        if type(csv_path) != Path:
            csv_path = Path(csv_path)

        with csv_path.open(newline='', encoding='utf-8') as fh:
            reader = csv.DictReader(fh)
            rows = [row for row in reader]

        datapoints = []
        for row in rows:
            name = row["name"]
            sequence = row["sequence"]
            ground_truth_type = row["ground_truth_type"]
            ground_truth_data = row["ground_truth_data"]
            if ground_truth_type in DataPoint.CHEMICAL_MAPPING_TYPES:
                spl = ground_truth_data.split(";")
                mapping = {}
                for item in spl:
                    pos, reactivity = item.split(":")
                    if reactivity == "":
                        continue
                    pos = int(pos)
                    reactivity = float(reactivity)
                    mapping[pos] = reactivity
                ground_truth_data = mapping
            if not ground_truth_type:
                ground_truth_type = "NONE"
            datapoint = DataPoint(name, sequence, ground_truth_type, ground_truth_data, cohort)
            datapoints.append(datapoint)

        return datapoints


    @staticmethod
    def extract_data_from_file(file_path):
        with open(file_path) as fh:
            data = [line.strip() for line in fh.readlines()]
        relevant_lines = []
        for d in data:
            if not d.startswith(";"):
                relevant_lines.append(d)

        return relevant_lines
