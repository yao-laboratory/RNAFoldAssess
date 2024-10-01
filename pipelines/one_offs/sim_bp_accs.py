import os


base = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/bprna/before_processing"

reps = [
    "Simfold_bpRNA-1m-90_0_lenience_report.txt",
    "Simfold_bpRNA-1m-90_1_lenience_report.txt"
]

for i, rep in enumerate(reps):
    with open(f"{base}/{rep}") as r:
        data = [d.split(", ") for d in r.readlines()]
    data.pop(0)
    sens = [float(d[6]) for d in data]
    ppvs = [float(d[7]) for d in data]
    f1s = [float(d[8]) for d in data]

    sen = sum(sens) / len(sens)
    ppv = sum(ppvs) / len(ppvs)
    f1 = sum(f1s) / len(f1s)

    print(f"Lenience {i}:")
    print(f"Data count: {len(sens)}")
    print(f"Sensitivty: {sen}")
    print(f"PPV: {ppv}")
    print(f"F1: {f1}")
    print()
