import os

from RNAFoldAssess.models import DataPoint
from RNAFoldAssess.models.scorers import *


headers = "algo_name, datapoint_name, sequence, prediction, accuracy, p_value"

def report_path(species, fname):
    return f"/mnt/nrdstor/yesselmanlab/ewhiting/reports/rasp_data/{species}/SPOT-RNA/SPOT-RNA_{fname}_predictions.txt"

def get_prediction(species, dp_name):
    dbn_path = f"/common/yesselmanlab/ewhiting/spot_outputs/rasp/{s}/dbn_files/{dp_name}.ct.dbn"
    if os.path.exists(dbn_path):
        with open(dbn_path) as fh:
            data = fh.readlines()
        dbn = data[-1].strip()
        return dbn
    else:
        return False


species = ["covid", "ecoli", "hiv"]
chem_map_method_map = {
    "covid": "SHAPE",
    "ecoli": "DMS",
    "hiv": "SHAPE"
}

for s in species:
    chemical_mapping_method = chem_map_method_map[s]
    print(f"Working {s}")
    if s == "hiv":
        species_folder = s.upper()
    else:
        species_folder = s
    json_path = f"/common/yesselmanlab/ewhiting/data/rasp_data/processed/{species_folder}"
    json_files = [f for f in os.listdir(json_path) if f.endswith(".json")]
    counter = 0
    for jf in json_files:
        print(f"\tWorking {jf}")
        report_string = f"{headers}\n"
        fname = jf.split(".")[0]
        generated_report_path = report_path(species_folder, fname)
        data_path = f"{json_path}/{jf}"
        dps = DataPoint.factory(data_path)
        for dp in dps:
            counter += 1
            if counter % 1234 == 0:
                print(f"\t\tWorking {counter}")
            if len(dp.sequence) <= 10:
                continue
            pred = get_prediction(s, dp.name)
            if not pred:
                continue
            try:
                if chemical_mapping_method == "DMS":
                    score = DSCI.score(
                        dp.sequence,
                        pred,
                        dp.reactivities,
                        DMS=True
                    )
                elif chemical_mapping_method == "SHAPE":
                    score = DSCI.score(
                        dp.sequence,
                        pred,
                        dp.reactivities,
                        SHAPE=True
                    )

                accuracy = score["accuracy"]
                p = score["p"]
                line_to_write = f"SPOT-RNA, {dp.name}, {dp.sequence}, {pred}, {p}\n"
                report_string += line_to_write
            except (DSCITypeError, DSCIValueError) as dsci_error:
                print(f"{dsci_error} on {dp.name}")
                continue

        with open(generated_report_path, "w") as fh:
            fh.write(report_string)

