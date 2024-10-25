import os


from RNAFoldAssess.models import DataPoint, EternaDataPoint
from RNAFoldAssess.models.scorers import *

# base_dir = "/work/yesselmanlab/ewhiting/spot_outputs"
# src_dir = f"{base_dir}/eterna"
# dest_dir = f"{base_dir}/eterna_remaining"
# existing = f"{base_dir}/eterna_dbn_files"

# existing_preds = [f.split(".")[0] for f in os.listdir(existing)]
# remaining = [f.split(".")[0] for f in os.listdir(src_dir)]

# with open(f"{base_dir}/to_be_transformed.txt", "w") as fh:
#     for rr in remaining:
#         if rr not in existing_preds:
#             fh.write(f"{rr}\n")

# print("Done")

data_points_path = "/common/yesselmanlab/ewhiting/data/translated_eterna_data/eterna.json"
datapoints = EternaDataPoint.factory(data_points_path)

shape_datapoints = []
dms_datapoints = []

fail_count = 0
for dp in datapoints:
    if dp.mapping_method == "SHAPE":
        shape_datapoints.append(dp)
    elif dp.mapping_method == "DMS":
        dms_datapoints.append(dp)
    else:
        print(f"Error in {dp.name}")
        fail_count += 1

print(f"There are {len(shape_datapoints)} SHAPE datapoints")
print(f"There are {len(dms_datapoints)} DMS datapoints")
print(f"There were {fail_count} errors detecting chemical mapping experiment type")
dms_tmp_report = open(
    "/mnt/nrdstor/yesselmanlab/ewhiting/reports/eterna_data/with_energy/SPOT_DMS_remaining.txt",
    "w"
)

shape_tmp_report = open(
    "/mnt/nrdstor/yesselmanlab/ewhiting/reports/eterna_data/with_energy/SPOT_SHAPE_remaining.txt",
    "w"
)

remaining_dir = f"/work/yesselmanlab/ewhiting/spot_outputs/eterna_remaining"
counter = 0
for dp in shape_datapoints:
    counter += 1
    if counter % 150 == 0:
        print(f"Working on {counter} of {len(shape_datapoints)}")

    try:
        with open(f"{remaining_dir}/{dp.name}.dbn") as fh:
            pred_data = fh.readlines()
            pred = pred_data[2].strip()

        score = dp.assess_prediction(pred)
        line_to_write = f"SPOT-RNA, {dp.name}, {dp.sequence}, {pred}, {score['accuracy']}, {score['p']}\n"
        shape_tmp_report.write(line_to_write)
    except FileNotFoundError:
        continue
    except Exception as e:
        print(f"Exception in {dp.name}: {e}")

for dp in dms_datapoints:
    counter += 1
    if counter % 150 == 0:
        print(f"Working on {counter} of {len(dms_datapoints)}")

    try:
        with open(f"{remaining_dir}/{dp.name}.dbn") as fh:
            pred_data = fh.readlines()
            pred = pred_data[2].strip()

        score = dp.assess_prediction(pred)
        line_to_write = f"SPOT-RNA, {dp.name}, {dp.sequence}, {pred}, {score['accuracy']}, {score['p']}\n"
        dms_tmp_report.write(line_to_write)
    except FileNotFoundError:
        continue
    except Exception as e:
        print(f"Exception in {dp.name}: {e}")
