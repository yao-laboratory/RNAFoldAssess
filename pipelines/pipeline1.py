import re, path, os


from RNAFoldAssess.models import DataPoint
from RNAFoldAssess.models.scorers import DSCI
from RNAFoldAssess.models.predictors import *


# Prepare data

data_path = "../data/development_data"

class Datum:
    def __init__(self, name, sequence, readings):
        self.name = name
        self.sequence = sequence
        self.readings = readings
        self.fix_readings()

    def fix_readings(self):
        readings = re.split("\t| ", self.readings)
        if len(readings) > 1:
            self.readings = []
            for read in readings:
                try:
                    self.readings.append(float(read))
                except:
                    continue

def datum_to_datapoint(datum):
    dhash = {
        "name": datum.name,
        "sequence": datum.sequence,
        "data": datum.readings,
        "reads": 0 # We don't use reads
    }
    return DataPoint(dhash)


f = open(data_path)
raw = f.read()
f.close()
raw = raw.split("\n\n")

data_points = []

for block in raw:
    name = ""
    sequence = ""
    readings = ""
    lines = block.split("\n")
    for line in lines:
        columns = line.split(":")
        if columns[0] == "Name":
            name = columns[1].strip()
        elif columns[0] == "Sequence":
            sequence = columns[1].strip()
        elif columns[0] == "Readings":
            readings = columns[1].strip()

    if (name and sequence and readings):
        data_points.append(Datum(name, sequence, readings))

data_problems = 0
for dp in data_points:
    # Making sure the lengths and sequences are working
    if len(dp.sequence) != len(dp.readings):
        data_problems += 1
        print(f"Something wrong with {dp.name}!!!!!")
        print(f"Sequence length: {len(dp.sequence)}, Readings length: {len(dp.readings)}")

if data_problems == 0:
    print("Data all good")
else:
    print(f"There were {data_problems} problems with the data")


# Transform to datapoints because I forgot the models expect that
dps = []
for dp in data_points:
    dps.append(datum_to_datapoint(dp))

if len(dps) == len(data_points):
    print("Successfully transformed datapoints")
else:
    print("Something went wrong in transofrmation")

# Prepare models

predictors = []
predictors.append({
    "name": "SPOT-RNA",
    "model": SPOT_RNA(),
    "path": path.Path("/home/yesselmanlab/ewhiting/SPOT-RNA").abspath()
})

predictors.append({
    "name": "Eterna",
    "model": Eterna(),
    "path": path.Path("/home/yesselmanlab/ewhiting/EternaFold").abspath()
})

predictors.append({
    "name": "MXFold",
    "model": MXFold(),
    "path": path.Path("/home/yesselmanlab/ewhiting/mxfold/build/mxfold").abspath()
})

# Run predictions
predictions = []
scores = []

# Run SPOT-RNA predictions
predictor = predictors[0]
for dp in dps:
    input_file_path = dp.to_fasta_file()
    predictor["model"].execute(predictor["path"], input_file_path, remove_file_when_done=True)
    prediction = predictor['model'].get_ss_prediction()
    scorer = DSCI(dp, prediction, "SPOT-RNA", evaluate_immediately=True, DMS=True)
    scores.append(scorer.metrics)

# Run Eterna prediction
predictor = predictors[1]
for dp in dps:
    input_file_path = dp.to_seq_file()
    predictor["model"].execute(predictor["path"], input_file_path)
    prediction = predictor["model"].get_ss_prediction()
    scorer = DSCI(dp, prediction, "Eterna", evaluate_immediately=True, DMS=True)
    scores.append(scorer.metrics)

# Run MXFold prediction
predictor = predictors[2]
for dp in dps:
    input_file_path = dp.to_fasta_file()
    predictor["model"].execute(predictor["path"], input_file_path)
    prediction = predictor['model'].get_ss_prediction()
    scorer = DSCI(dp, prediction, "MXFold", evaluate_immediately=True, DMS=True)
    scores.append(scorer.metrics)

print("\nPrinting scores\n")
for s in scores:
    print(s)



