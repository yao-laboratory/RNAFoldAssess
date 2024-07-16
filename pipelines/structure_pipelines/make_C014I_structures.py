import os


from RNAFoldAssess.models import DataPoint

max_structures = 5
pval_cutoff = 0.05
max_iterations = 1000

structure_path = "/work/yesselmanlab/ewhiting/reverse_experiment/scores/C014I"
destination = "/work/yesselmanlab/ewhiting/C014I_structures"

dp_file_path = "/common/yesselmanlab/ewhiting/ss_deeplearning_data/data"
datapoints = dps = DataPoint.factory(f"{dp_file_path}/C014I.json", "C014I")

for dp in datapoints:
    try:
        with open(f"{structure_path}/{dp.name}.txt") as f:
            data = f.readlines()
        wfname = f"{dp.name}.stc"
        structures = []
        iteration = 0
        for d in data:
            d = d.split(", ")
            stc = d[2]
            acc = float(d[3])
            p = float(d[4].strip())
            if acc == 1.0 and p <= pval_cutoff and len(structures) < max_structures:
                structures.append(stc)
            if len(structures) >= max_structures:
                break
            iteration += 1
            if iteration >= max_iterations:
                break
        if len(structures) > 0:
            wf = open(f"{destination}/{wfname}", "w")
            wf.write(f"{dp.sequence}\n")
            for stc in structures:
                wf.write(f"{stc}\n")
            reacs = ",".join([str(r) for r in dp.reactivities])
            wf.write(f"{reacs}\n")
            wf.close()
    except FileNotFoundError:
        print(f"Couldn't find file for {dp.name}")
        continue

