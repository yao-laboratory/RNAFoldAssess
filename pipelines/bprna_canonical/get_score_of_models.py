import os


report_dir = "/work/yesselmanlab/ewhiting/bprna_canonical_reports"

models = [
    "ContextFold",
    "ContraFold",
    "EternaFold",
    "IPKnot",
    "MXFold",
    "MXFold2",
    "NeuralFold",
    "NUPACK",
    "pKnots",
    "RNAFold",
    "RNAStructure",
    "Simfold",
    "SPOT-RNA"
]

for m in models:
    msg_string = f"{m},"
    for lenience in [0, 1]:
        fname = f"{m}_master_{lenience}_lenience.txt"
        with open(f"{report_dir}/{fname}") as fh:
            data = fh.readlines()
        data.pop(0)
        data = [d.split(", ") for d in data]
        # 6, 7, 8
        n = len(data)
        msg_string += f"{n},"

        sens = [float(d[6]) for d in data]
        sen = sum(sens) / len(sens)
        msg_string += f"{sen},"

        ppvs = [float(d[7]) for d in data]
        ppv = sum(ppvs) / len(ppvs)
        msg_string += f"{ppv},"

        f1s = [float(d[8]) for d in data]
        f1 = sum(f1s) / len(f1s)
        msg_string += f"{f1},"

    print(msg_string)
