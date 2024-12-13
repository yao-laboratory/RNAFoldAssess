import os


base_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/crystal_release_2024"
dest_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions"

models = [
    ("ContextFold", {"sensitivity": 6, "ppv": 7, "f1": 8}),
    ("ContraFold", {"sensitivity": 6, "ppv": 7, "f1": 8}),
    ("EternaFold", {"sensitivity": 6, "ppv": 7, "f1": 8}),
    ("IPKnot", {"sensitivity": 6, "ppv": 7, "f1": 8}),
    ("Neuralfold", {"sensitivity": 5, "ppv": 6, "f1": 7}),
    ("NUPACK", {"sensitivity": 6, "ppv": 7, "f1": 8}),
    ("RNAFold", {"sensitivity": 6, "ppv": 7, "f1": 8}),
    ("RNAStructure", {"sensitivity": 6, "ppv": 7, "f1": 8}),
    ("pKnots", {"sensitivity": 5, "ppv": 6, "f1": 7}),
    ("Simfold", {"sensitivity": 5, "ppv": 6, "f1": 7}),
    ("MXFold", {"sensitivity": 6, "ppv": 7, "f1": 8}),
    ("MXFold2", {"sensitivity": 5, "ppv": 6, "f1": 7}),
    ("SPOT-RNA", {"sensitivity": 5, "ppv": 6, "f1": 7}),
]


# 6, 7, 8

for lenience in [0, 1]:
    print(f"Working lenience {lenience}")
    all_preds = []
    for m, kv_pair in models:
        print(f"\tWorking mdoel {m}")
        with open(f"{base_dir}/{m}_predictions_{lenience}_lenience.txt") as fh:
            data = fh.readlines()
        data.pop(0)
        all_preds += data
        data = [d.split(", ") for d in data]
        for stat, index in kv_pair.items():
            stats = [d[index].strip() for d in data]
            with open(f"pdb_acc_files/{m}_{stat}_{lenience}.txt", "w") as fh:
                fh.write(",".join(stats))
    with open(f"{dest_dir}/pdb_master_{lenience}_lenience.txt", "w") as fh:
        for pred in all_preds:
            fh.write(pred)

