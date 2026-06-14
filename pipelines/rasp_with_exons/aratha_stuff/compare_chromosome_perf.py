import os


report_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/rasp_data/ara-tha/canonical"
models = [
    'IPKnot',
    'MXFold2',
    'SPOT-RNA',
    'RNAStructure',
    'pKnots',
    'Simfold',
    'NeuralFold',
    'EternaFold',
    'MXFold',
    'ContextFold',
    'ContraFold',
    'RNAFold',
    'NUPACK'
]

chromosomes = ["1", "2", "3", "4", "5", "Mt", "Pt"]

model_chr_map = {}
for m in models:
    model_chr_map[m] = {}
    for ch in chromosomes:
        model_chr_map[m][ch] = []


for m in models:
    with open(f"{report_dir}/{m}_ara-tha_predictions.txt") as fh:
        lines = fh.readlines()

    lines = [line.split(", ") for line in lines]
    for line in lines:
        dp = line[1]
        ch = dp.split("_")[0]
        acc = float(line[4])
        model_chr_map[m][ch].append(acc)

for ch in chromosomes:
    print(f"For Chromosome {ch} - ")
    for m in models:
        accs = model_chr_map[m][ch]
        if len(accs) == 0:
            print(f"\tNothing for {m}")
            continue
        avg = sum(accs) / len(accs)
        print(f"\t{m}: {round(avg, 4)} (n = {len(accs)})")
    print()

