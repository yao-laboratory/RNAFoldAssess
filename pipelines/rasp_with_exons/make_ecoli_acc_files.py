import os


base_report_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/rasp_data"
species = "ecoli"
report_dir = f"{base_report_dir}/{species}"
models = [
    "ContextFold",
    "ContraFold",
    "EternaFold",
    "IPKnot",
    "NeuralFold",
    "NUPACK",
    "RNAFold",
    "RNAStructure",
    "pKnots",
    "Simfold",
    "MXFold",
    "MXFold2",
    "SPOT-RNA"
]

dest_dir = f"/home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/rasp_with_exons/acc_files/{species}"
dp_acc_map = {}

for m in models:
    print(f"Working {m}")
    model_accs = []
    if m in ["NeuralFold", "RNAStructure", "pKnots", "Simfold", "MXFold2", "SPOT-RNA", "NUPACK"]:
        m_report_dir = f"{report_dir}/{m}"
    else:
        m_report_dir = f"{report_dir}/{m}/filtered"
    files = [f for f in os.listdir(m_report_dir) if f.startswith(f"{m}_") and "prediction" in f]
    for f in files:
        with open(f"{m_report_dir}/{f}") as fh:
            data = fh.readlines()
        
        if len(data) <= 0:
            continue

        if data[0].startswith("algo"):
            data.pop(0)
        
        data = [d.split(", ") for d in data]
        accs = [d[4] for d in data]
        model_accs += accs
    
    with open(f"{dest_dir}/{m}_accs.txt", "w") as fh:
        fh.write(",".join(model_accs))
