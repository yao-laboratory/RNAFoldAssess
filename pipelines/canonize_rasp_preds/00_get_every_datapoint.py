import os, json


dp_base = {
    "RASP-Arabidopsis": "/mnt/nrdstor/yesselmanlab/ewhiting/data/rasp_data/ara-tha/json_files",
    "RASP-COVID": "/mnt/nrdstor/yesselmanlab/ewhiting/data/rasp_data/processed/covid/rasp_covid_chromosome_NC_045512.2.json",
    "RASP-ecoli": "/mnt/nrdstor/yesselmanlab/ewhiting/data/rasp_data/processed/ecoli/round_2/rasp_ecoli_chromosome_U00096.2.json",
    "RASP-HIV": "/mnt/nrdstor/yesselmanlab/ewhiting/data/rasp_data/processed/HIV",
    "RASP-Human": "/mnt/nrdstor/yesselmanlab/ewhiting/data/rasp_data/human/json_files",
}

chem_map_method_map = {
    "RASP-Arabidopsis": "DMS",
    "RASP-COVID": "SHAPE",
    "RASP-ecoli": "DMS",
    "RASP-HIV": "SHAPE",
    "RASP-Human": "DMS"
}

gt_map = {"RASP-Arabidopsis": "reactivity_map",
          "RASP-COVID": "reactivities",
          "RASP-ecoli": "reactivities",
          "RASP-HIV": "reactivities",
          "RASP-Human": "reactivity_map"}

def return_rasp_datapoints(location, species):
    if location.endswith(".json"):
        with open(location) as fh:
            data = json.load(fh)
    else:
        json_files = os.listdir(location)
        data = []
        for jf in json_files:
            with open(f"{location}/{jf}") as fh:
                data += json.load(fh)
    dps = []
    for d in data:
        keys = list(d.keys())
        name = d["name"]
        sequence = d["sequence"].upper().replace("T", "U")
        if "chem_map_type" in keys:
            experiment_type = d["chem_map_type"]
        else:
            if species in ["RASP-COVID", "RASP-HIV"]:
                experiment_type = "SHAPE"
            else:
                experiment_type = "DMS"

        dp = {"name": name, "sequence": sequence, "experiment_type": experiment_type}

        if "reactivity_map" in keys:
            reactivity_map = d["reactivity_map"]
            dp["reactivity_map"] = reactivity_map
        else:
            dp["reactivities"] = d["data"]
        dps.append(dp)

    return dps


fstring = "dataset;rna_id;sequence;chem_map_method;ground_truth\n"
for ds, loc in dp_base.items():
    chem_map_method = chem_map_method_map[ds]
    datapoints = return_rasp_datapoints(loc, ds)
    ground_truth_key = gt_map[ds]
    for dp in datapoints:
        line = f"{ds};{dp['name']};{dp['sequence']};{chem_map_method};{dp[ground_truth_key]}\n"
        fstring += line

destination_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/consolidated"
with open(f"{destination_dir}/RASP_all_datapoints.csv", "w") as fh:
    fh.write(fstring)

print("Done")
