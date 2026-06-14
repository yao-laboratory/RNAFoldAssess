import os, json


dp_data_loc = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/consolidated"

chem_map_pred_map = {
    "EternaBench": "/mnt/nrdstor/yesselmanlab/ewhiting/reports/eterna_data/with_energy/canonical",
    "Ribonanza": "/mnt/nrdstor/yesselmanlab/ewhiting/reports/ribonanza/canonical",
    "RNAndria-miRNA": "/mnt/nrdstor/yesselmanlab/ewhiting/reports/rnandria/canonical",
    "RNAndria-mRNA": "/mnt/nrdstor/yesselmanlab/ewhiting/reports/rnandria/canonical",
    "YData": "/mnt/nrdstor/yesselmanlab/ewhiting/reports/ydata/canonize"
}

datasets = list(chem_map_pred_map.keys())

models = ["ContextFold", "ContraFold", "EternaFold", "IPKnot",
          "NeuralFold", "NUPACK", "RNAFold",
          "RNAStructure", "pKnots", "Simfold",
          "MXFold", "MXFold2", "SPOT-RNA"]

print("Making initial datapoint map")
dp_map = {}

for ds in datasets:
    with open(f"{dp_data_loc}/{ds}_all_datapoints.csv") as fh:
        data = fh.readlines()
    
    data.pop(0)
    counter = 0
    for d in data:
        counter += 1
        if counter % 100000 == 0:
            print(f"Working {counter}")
        d = d.strip()
        d = d.split(";")
        dp_name = d[1]
        sequence = d[2]
        reactivities = d[3]
        reactivities = eval(reactivities)
        try:
            if type(reactivities[0]) is tuple:
                data_type = "reactivity_map"
                reactivities = [list(r) for r in reactivities]
            else:
                data_type = "reactivities"
        except IndexError:
            print()
            print(f"Index error at {counter}")
            print(f"Reactivities: {reactivities}")
            print(f"Whole line: {d}")
            print()
            continue
        
        dp_map[dp_name] = {
            "seq": sequence,
            "dataset": ds,
            "data": reactivities,
            "data_type": data_type,
            "preds": {}
        }

        for m in models:
            dp_map[dp_name]["preds"][m] = {}


def get_files(ds):
    loc = chem_map_pred_map[ds]
    if ds == "RNAndria-miRNA":
        files = [f for f in os.listdir(loc) if "miRNA" in f]
    elif ds == "RNAndria-mRNA":
        files = [f for f in os.listdir(loc) if "mRNA" in f]
    else:
        files = os.listdir(loc)
    
    return files


print("Assembling prediction map")
for ds in datasets:
    misses = 0
    print(f"Working {ds}")
    files = get_files(ds)
    ds_dir = chem_map_pred_map[ds]
    for f in files:
        with open(f"{ds_dir}/{f}") as fh:
            lines = fh.readlines()
        
        if lines[0].startswith("algo"):
            lines.pop(0)
        
        lines = [line.split(", ") for line in lines]
        model = lines[0][0]
        for line in lines:
            try:
                dp = line[1]
                pred = line[3]
                acc = float(line[4])
                dp_map[dp]["preds"][model]["prediction"] = pred
                dp_map[dp]["preds"][model]["score"] = acc
            except KeyError:
                misses += 1
                print(f"Missed {misses}")
                continue

print("Writing json file")
dest_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions"
with open(f"{dest_dir}/chem_map_preds_and_scores.json", "w") as fh:
    json.dump(dp_map, fh)

