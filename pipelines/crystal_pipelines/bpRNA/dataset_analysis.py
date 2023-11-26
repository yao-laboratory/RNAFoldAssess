import os

dbn_path = "/common/yesselmanlab/ewhiting/data/bprna/dbnFiles"

files = os.listdir(dbn_path)
flen = len(files)

types = {}

print(f"Starting work on {flen} files")
counter = 0
for f in files:
    if counter % 250 == 0:
        print(f"Starting {counter} of {flen} ...")
    kind_of_file = f.split("bpRNA_")[1].split("_")[0]
    counter += 1
    try:
        types[kind_of_file] += 1
    except KeyError:
        types[kind_of_file] = 1


for t in types:
    print(f"Number of {t} dbn files: {types[t]}")

print()

# Number of CRW dbn files: 55,600
# Number of RFAM dbn files: 43,273
# Number of SRP dbn files: 959
# Number of SPR dbn files: 623
# Number of tmRNA dbn files: 728
# Number of PDB dbn files: 669
# Number of RNP dbn files: 466
