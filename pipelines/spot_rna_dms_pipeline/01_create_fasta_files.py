import os, datetime

# Going to have to do this a stupid way because of conda shenanigans

from RNAFoldAssess.models import DataPoint

dp_path = "/common/yesselmanlab/ewhiting/ss_deeplearning_data/data"
data_point_files = os.listdir(dp_path)

print(f"Loading data points from {len(data_point_files)} files ...")

data_points = []
for dpf in data_point_files:
    cohort = dpf.split(".")[0]
    print(f"Loading data points from {cohort} cohort")
    dps = DataPoint.factory(f"{dp_path}/{dpf}", cohort)
    for dp in dps:
        data_points.append(dp)

data_destination = "/common/yesselmanlab/ewhiting/data/dp_fasta"

counter = 0
dp_len = len(dps)
for dp in data_points:
    if counter % 250 == 0:
        print(f"Done {counter} of {dp_len}")
    os.system(f"mkdir {data_destination}/{dp.cohort}")
    name = dp.name.replace(" ", "_")
    data = f">{name}\n{dp.sequence}"
    f = open(f"{data_destination}/{dp.cohort}/{name}.fasta", "w")
    f.write(data)
    f.close()
    counter += 1
