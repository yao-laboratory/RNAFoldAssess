import os, json


prefix = "rasp_human_chromosome"
suffix = ".json"

json_path = "/common/yesselmanlab/ewhiting/data/rasp_data/human/processed"
base_path = "/common/yesselmanlab/ewhiting/data/rasp_data/human"
seq_path = f"{base_path}/sequences"
cooordinate_path = f"{base_path}/coordinate_files"


print("Assembling datapoints")
ch_dp_map = {}
json_files = [f for f in os.listdir(json_path) if f.endswith(".json")]

