import os


report_dir = "/common/yesselmanlab/ewhiting/reports/eterna_data"

all_files = os.listdir(report_dir)

dms_files = [f for f in all_files if "MXFold2_partition" in f]
dms_files = [f for f in dms_files if "DMS_pipeline_report" in f]

shape_files = [f for f in all_files if "MXFold2_partition" in f]
shape_files = [f for f in shape_files if "SHAPE_pipeline_report" in f]


all_dms_data = []
for df in dms_files:
    f = open(f"{report_dir}/{df}")
    data = f.readlines()
    f.close()
    data.pop(0)
    all_dms_data += data

all_shape_data = []
for sf in shape_files:
    f = open(f"{report_dir}/{sf}")
    data = f.readlines()
    f.close()
    data.pop(0)
    all_shape_data += data

dms_file = "MXFold2_DMS_pipeline_report.txt"
shape_file = "MXFold2_SHAPE_pipeline_report.txt"

df = open(f"{report_dir}/{dms_file}", "w")
for d in all_dms_data:
    df.write(d)
df.close()

sf = open(f"{report_dir}/{shape_file}", "w")
for d in all_shape_data:
    sf.write(d)
sf.close()
