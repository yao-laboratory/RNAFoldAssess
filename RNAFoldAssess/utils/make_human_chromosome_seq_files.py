import os


seq_file = "/common/yesselmanlab/ewhiting/data/rasp_data/human/hg38.fa"
base_path = "/common/yesselmanlab/ewhiting/data/rasp_data/human"
seq_path = f"{base_path}/sequences"

if not os.path.exists(seq_path):
    os.mkdir(seq_path)

acceptable_chromosomes = [f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"]
ch_seq_map = {}

for ch in acceptable_chromosomes:
    ch_seq_map[ch] = []

with open(seq_file) as fh:
    fa_lines = fh.readlines()


chromosome = fa_lines.pop(0).strip().replace(">", "")
print(f"Working chromosome {chromosome}")
for line in fa_lines:
    if line.startswith(">"):
        chromosome = line.strip().replace(">", "")
        print(f"Working chromosome {chromosome}")

    if chromosome in acceptable_chromosomes:
        ch_seq_map[chromosome].append(line.strip())

# For testing
print(f"There are {len(ch_seq_map)} choromosomes found")

for ch in ch_seq_map:
    path = f"{seq_path}/{ch}.seq"
    sequences = ch_seq_map[ch]
    fstring = "\n".join(sequences)
    with open(path, "w") as fh:
        fh.write(fstring)

print("Done")
