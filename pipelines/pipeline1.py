import re


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

problems = 0
for dp in data_points:
    # Making sure the lengths and sequences are working
    if len(dp.sequence) != len(dp.readings):
        print(f"Something wrong with {dp.name}!!!!!")
        print(f"Sequence length: {len(dp.sequence)}, Readings length: {len(dp.readings)}")
if problems == 0:
    print("All good")
else:
    print(f"There were {problems} problems")


