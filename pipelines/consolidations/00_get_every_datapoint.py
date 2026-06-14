import os, json


from RNAFoldAssess.models import DataPoint, EternaDataPoint, DataPointFromCrystal


destination_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/consolidated"

ribo_experiment_map = {
    "BzCN_cotx": "DMS4",
    "DMS_M2_seq": "DMS4",
    "DMS_cotx": "DMS4",
    "DMS": "DMS4",
    "1M7": "SHAPE",
    "NMIA": "SHAPE",
    "BzCN": "SHAPE",
    "deg_Mg_50C": "SHAPE",
    "deg_50C": "SHAPE",
    "deg_pH10": "SHAPE",
    "deg_Mg_pH10": "SHAPE",
    "CMCT": "CMCT"
}

dp_base = {
    "EternaBench": "/mnt/nrdstor/yesselmanlab/ewhiting/data/translated_eterna_data/eterna.json",
    "Ribonanza": "/mnt/nrdstor/yesselmanlab/ewhiting/rna_data/ribonanza/rmdb_data.v1.3.0.csv",
    "RNAndria-miRNA": "/mnt/nrdstor/yesselmanlab/ewhiting/data/rnandria/rnandria_data_JSON/processed/pri_miRNA_datapoints.json",
    "RNAndria-mRNA": "/mnt/nrdstor/yesselmanlab/ewhiting/data/rnandria/rnandria_data_JSON/processed/human_mRNA_datapoints.json",
    "YData": "/mnt/nrdstor/yesselmanlab/ewhiting/ss_deeplearning_data/data",
    "PDB": "/mnt/nrdstor/yesselmanlab/ewhiting/data/crystal_all/release_2024/long_dbns",
    "bp-RNA": "/work/yesselmanlab/ewhiting/data/bprna/dbnFiles",
    "RASP-Arabidopsis": "/mnt/nrdstor/yesselmanlab/ewhiting/data/rasp_data/ara-tha/json_files",
    "RASP-COVID": "/mnt/nrdstor/yesselmanlab/ewhiting/data/rasp_data/processed/covid/rasp_covid_chromosome_NC_045512.2.json",
    "RASP-ecoli": "/mnt/nrdstor/yesselmanlab/ewhiting/data/rasp_data/processed/ecoli/round_2/rasp_ecoli_chromosome_U00096.2.json",
    "RASP-HIV": "/mnt/nrdstor/yesselmanlab/ewhiting/data/rasp_data/processed/HIV",
    "RASP-Human": "/mnt/nrdstor/yesselmanlab/ewhiting/data/rasp_data/human/json_files",
}

dp_base_chem_map = {
    "EternaBench": "/mnt/nrdstor/yesselmanlab/ewhiting/data/translated_eterna_data/eterna.json",
    "Ribonanza": "/mnt/nrdstor/yesselmanlab/ewhiting/rna_data/ribonanza/rmdb_data.v1.3.0.csv",
    "RNAndria-miRNA": "/mnt/nrdstor/yesselmanlab/ewhiting/data/rnandria/rnandria_data_JSON/processed/pri_miRNA_datapoints.json",
    "RNAndria-mRNA": "/mnt/nrdstor/yesselmanlab/ewhiting/data/rnandria/rnandria_data_JSON/processed/human_mRNA_datapoints.json",
    "YData": "/mnt/nrdstor/yesselmanlab/ewhiting/ss_deeplearning_data/data"
}

gt_map = {
    "EternaBench": "reactivity_map",
    "Ribonanza": "reactivity_map",
    "RNAndria-miRNA": "reactivities",
    "RNAndria-mRNA": "reactivities",
    "YData": "reactivities",
    "PDB": "true_structure",
    "bp-RNA": "dbn",
    "RASP-Arabidopsis": "reactivity_map",
    "RASP-COVID": "reactivities",
    "RASP-ecoli": "reactivities",
    "RASP-HIV": "reactivities",
    "RASP-Human": "reactivity_map",
}


def return_datapoints(ds_name, location):
    if ds_name == "EternaBench":
        obj_dps = EternaDataPoint.factory(location)
        dps = [odp.__dict__ for odp in obj_dps]
    elif ds_name == "Ribonanza":
        dps = return_ribo_datapoints(location)
    elif "RNAndria" in ds_name:
        obj_dps = DataPoint.factory(location)
        dps = [odp.__dict__ for odp in obj_dps]
    elif ds_name == "YData":
        obj_dps = return_ydata_datapoints(location)
        dps = [odp.__dict__ for odp in obj_dps]
    elif ds_name == "bp-RNA":
        dps = return_bprna_datapoints(location)
    elif ds_name == "PDB":
        obj_dps = DataPointFromCrystal.factory_from_dbn_files(location)
        dps = [odp.__dict__ for odp in obj_dps]
    elif ds_name.startswith("RASP"):
        dps = return_rasp_datapoints(location, ds_name)
    return dps




def return_ribo_datapoints(location):
    with open(location) as fh:
        data = fh.readlines()
    data.pop(0)
    data = [d.split(",") for d in data]
    r1_index = 7
    dps = []
    for d in data:
        name = d[0]
        seq = d[1]
        experiment_type = d[2]
        chemical_mapping_method = ribo_experiment_map[experiment_type]
        reactivities = d[r1_index:len(seq) + r1_index]
        reactivity_map = []
        for i, reactivity in enumerate(reactivities):
            if reactivity != "":
                reactivity_map.append((i, reactivity))

        dps.append({
            "name": name,
            "sequence": seq,
            "experiment_type": chemical_mapping_method,
            "reactivity_map": reactivity_map
        })
    return dps


def return_ydata_datapoints(location):
    approved_cohorts = [
        "C014G",
        "C014H",
        "C014I",
        "C014J",
        "C014U",
        "C014V"
    ]

    dp_files = os.listdir(location)
    dp_files = [df for df in dp_files if df.split(".")[0] in approved_cohorts]
    dps = []
    for df in dp_files:
        cohort = df.split(".")[0]
        path = f"{location}/{df}"
        dps += DataPoint.factory(path, cohort)

    return dps


def return_bprna_datapoints(location):
    dbn_files = [f for f in os.listdir(location) if f.endswith(".dbn")]
    dps = []
    for df in dbn_files:
        with open(f"{location}/{df}") as fh:
            data = fh.readlines()

        name = df.split(".")[0]
        seq = data[3].strip()
        dbn = data[4].strip()

        dbn = list(dbn)
        new_dbn = ""
        for nt in dbn:
            if nt not in "().":
                new_dbn += "."
            else:
                new_dbn += nt
        dps.append({
            "name": name,
            "sequence": seq,
            "dbn": new_dbn
        })

    return dps


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


headers = "dataset;rna_id;sequence;ground_truth\n"
def write_report():
    all_datapoints = {}
    for ds, loc in dp_base.items():
        ground_truth_key = gt_map[ds]
        f = open(f"{destination_dir}/{ds}_all_datapoints.csv", "w")
        f.write(headers)
        print(f"Getting datapoints for {ds}")
        datapoints = return_datapoints(ds, loc)
        len_dp = len(datapoints)
        counter = 0
        for dp in datapoints:
            counter += 1
            if counter % 2500 == 0:
                print(f"Writing {counter} of {len_dp} in {ds} ...")
            line = f"{ds};{dp['name']};{dp['sequence']};{dp[ground_truth_key]}\n"
            f.write(line)
        f.close()

write_report()
