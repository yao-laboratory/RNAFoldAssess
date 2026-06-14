import json


base_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions"
json_file_path = f"{base_dir}/chem_map_preds_and_scores.json"
easy_dp_file = f"{base_dir}/easy_chem_map_datapoints.txt"
hard_dp_file = f"{base_dir}/hard_chem_map_datapoints.txt"

print("Opening files")
with open(easy_dp_file) as fh:
    easy_dps = [line.strip() for line in fh.readlines()]

with open(hard_dp_file) as fh:
    hard_dps = [line.strip() for line in fh.readlines()]

with open(json_file_path) as fh:
    data = json.load(fh)

def get_gc_content(seq):
    seq = seq.upper()
    gc_count = seq.count("G") + seq.count("C")
    return gc_count / len(seq)

csv_map = {
    "easy": easy_dps,
    "hard": hard_dps
}

models = ["ContextFold", "ContraFold", "EternaFold", "IPKnot",
          "NeuralFold", "NUPACK", "RNAFold",
          "RNAStructure", "pKnots", "Simfold",
          "MXFold", "MXFold2", "SPOT-RNA"]

headers = "datapoint,sequence,length,gc_content,"
model_items = []
for m in models:
    model_items.append(f"{m}_pred")
    model_items.append(f"{m}_score")

headers += ",".join(model_items) + "\n"

# data['ETOBCR_VN1_0001_ANNOTATION_1']
# {'seq': 'ACUG', 'dataset': 'EternaBench',
# 'data': [[9, 0], [10, 0.4967], [11, 0.3316], [12, 0.3635]],
# 'data_type': 'reactivity_map',
# 'preds': {
#     'ContextFold': {'prediction': '....', 'score': 0.5743243243243243},
#     'ContraFold': {'prediction': '.(.)', 'score': 0.5788409703504043},
#     # etc
#     }
# }

def get_line(dp):
    dp_data = data[dp]
    line = f"{dp},{dp_data['seq']},"
    seq_len = len(dp_data['seq'])
    gc_content = get_gc_content(dp_data['seq'])
    line += f"{seq_len},{gc_content},"
    preds = dp_data['preds']
    m_items = []
    for m in models:
        m_items.append(preds[m]["prediction"])
        m_items.append(str(preds[m]["score"]))
    line += ",".join(m_items) + "\n"
    return line


for dp_type, datapoints in csv_map.items():
    print(f"Making {dp_type} CSV")
    csv_file = open(f"{base_dir}/chem_map_{dp_type}_master.csv", "w")
    csv_file.write(headers)
    for dp in datapoints:
        line = get_line(dp)
        csv_file.write(line)
    csv_file.close()

print("Done")
