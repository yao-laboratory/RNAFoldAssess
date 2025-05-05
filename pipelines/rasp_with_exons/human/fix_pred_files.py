import os


base_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/rasp_data/human"
fixed_files_dir = f"{base_dir}/fixed_files"

models = [
    # "ContextFold",
    # "ContraFold",
    # "EternaFold",
    # "IPKnot",
    # "MXFold",
    # "MXFold2",
    # "NeuralFold",
    "NUPACK",
    # "pKnots",
    # "RNAFold",
    # "RNAStructure",
    # "Simfold",
    # "SPOT-RNA"
]

headers = "algo_name, datapoint_name, sequence, prediction, accuracy, p_value\n"

for m in models:
    print(f"Working {m}")
    pred_files = [f for f in os.listdir() if f"{m}_chr" in f]

    data = []
    for f in pred_files:
        with open(f"{base_dir}/{f}") as fh:
            lines = fh.readlines()

        if len(lines) <= 1:
            continue
        lines.pop(0)
        data += lines

    unique_lines = ""
    datapoints_addressed = set()

    data = [d.split(", ") for d in data]
    for d in data:
        if len(d) <= 1:
            continue
        name = d[1]
        if name in datapoints_addressed:
            continue
        datapoints_addressed.add(name)
        unique_lines += ", ".join(d)

    print(f"\tWriting {len(datapoints_addressed)} unique datapoints to {m} report")

    with open(f"{fixed_files_dir}/{m}_all_preds.txt", "w") as fh:
        fh.write(unique_lines)
