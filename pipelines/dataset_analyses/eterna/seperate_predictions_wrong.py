from RNAFoldAssess.utils.secondary_structure_tools import SecondaryStructureTools


lowest_quartile = 0.6293

base_dir = "/common/yesselmanlab/ewhiting/reports/eterna_data"

def shape_file_name(model_name):
    return f"{base_dir}/{model_name}_SHAPE_pipeline_report.txt"

def dms_file_name(model_name):
    return f"{base_dir}/{model_name}_DMS_pipeline_report.txt"

models = [
    "ContextFold",
    "ContraFold",
    "EternaFold",
    "IPKnot",
    "MXFold",
    "RandomPredictor",
    "RNAFold",
    "SeqFold"
]

destination_dir = "/common/yesselmanlab/ewhiting/dataset_analyses/eterna"
good_guesses = open(f"{destination_dir}/EternaData_good_guesses_with_energy.txt", "w")
bad_guesses = open(f"{destination_dir}/EternaData_bad_guesses_with_energy.txt", "w")

for m in models:
    print(f"Working {m}")
    # Get SHAPE predictions
    shape_path = shape_file_name(m)
    sf = open(shape_path)
    data = sf.readlines()
    sf.close()
    # Get rid of headers
    data.pop(0)
    for d in data:
        d = d.strip()
        d = d.split(", ")
        seq = d[2]
        stc = d[3]
        acc = float(d[4])
        fe = SecondaryStructureTools.get_free_energy(seq, stc)
        d = ", ".join(d)
        d += f", {fe}\n"
        if acc <= lowest_quartile:
          bad_guesses.write(d)
        else:
          good_guesses.write(d)
    # Get DMS predictions
    dms_path = dms_file_name(m)
    df = open(dms_path)
    data = df.readlines()
    df.close()
    # Get rid of headers
    data.pop(0)
    for d in data:
        d = d.strip()
        d = d.split(", ")
        seq = d[2]
        stc = d[3]
        acc = float(d[4])
        fe = SecondaryStructureTools.get_free_energy(seq, stc)
        d = ", ".join(d)
        d += f", {fe}\n"
        if acc <= lowest_quartile:
          bad_guesses.write(d)
        else:
          good_guesses.write(d)

good_guesses.close()
bad_guesses.close()


