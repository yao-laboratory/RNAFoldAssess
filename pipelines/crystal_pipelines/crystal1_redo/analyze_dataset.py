import os


base_dir = "/common/yesselmanlab/ewhiting/data/crystal1_XRAY"
ss_dir = f"{base_dir}/redo_analysis/secondary_structures"
prep_dir = f"{ss_dir}/preprocessed"

raw_dbns = [dbn for dbn in os.listdir(ss_dir) if dbn.endswith("dbn")]
prep_dbns = [dbn for dbn in os.listdir(prep_dir) if dbn.endswith("dbn")]


# Get discared PDBs
base_pdbs_in_prep = set()
for dbn in prep_dbns:
    base_pdbs_in_prep.add(dbn[:4])


# Analyze discareded PDBs
discared = []
for dbn in raw_dbns:
    if dbn[:4] not in base_pdbs_in_prep:
        discared.append(dbn)

discared_count = len(discared)
print(f"There are {discared_count} PDBs left out")


chain_counts = []
seq_lens = []
for dbn in discared:
    f = open(f"{ss_dir}/{dbn}")
    lines = f.readlines()
    f.close()
    seq = lines[1].strip()
    chains = len(seq.split("&"))
    chain_counts.append(chains)
    seq_len = len(seq.replace("&", ""))
    seq_lens.append(seq_len)


print("Chains:")
print(f"Most chains: {max(chain_counts)}")
print(f"\t{chain_counts.count(max(chain_counts))} occurences")
print(f"Least chains: {min(chain_counts)}")
print(f"\t{chain_counts.count(min(chain_counts))} occurences")
print(f"Average chain count: {sum(chain_counts) / len(chain_counts)}")

print("Sequences:")
print(f"Most sequences: {max(seq_lens)}")
print(f"\t{seq_lens.count(max(seq_lens))} occurences")
print(f"Least sequences: {min(seq_lens)}")
print(f"\t{seq_lens.count(min(seq_lens))} occurences")
print(f"Average sequence count: {sum(seq_lens) / len(seq_lens)}")


# Analyze chain dataset

cutoff1 = 2
cutoff2 = 4
cutoff3 = 8
cutoff4 = 16
cutoff5 = 24

c1_count = 0
c2_count = 0
c3_count = 0
c4_count = 0
c5_count = 0
big_count = 0

lengths = []

for dbn in prep_dbns:
    f = open(f"{prep_dir}/{dbn}")
    lines = f.readlines()
    f.close()
    seq = lines[1]
    seq_len = len(seq)
    lengths.append(seq_len)
    if seq_len <= cutoff1:
        c1_count += 1
    if seq_len > cutoff1 and seq_len <= cutoff2:
        c2_count += 1
    if seq_len > cutoff2 and seq_len <= cutoff3:
        c3_count += 1
    if seq_len > cutoff3 and seq_len <= cutoff4:
        c4_count += 1
    if seq_len > cutoff4 and seq_len <= cutoff5:
        c5_count += 1
    if seq_len > cutoff5:
        big_count += 1

avg_len = sum(lengths) / len(lengths)
max_len = max(lengths)
min_len = min(lengths)

print("Sequences in chain-based dataset:")
print(f"Average sequence length: {avg_len}")
print(f"Max sequence length: {max_len}")
print(f"Min sequence length: {min_len}")
print(f"Cutoff 1 count: {c1_count}")
print(f"Cutoff 2 count: {c2_count}")
print(f"Cutoff 3 count: {c3_count}")
print(f"Cutoff 4 count: {c4_count}")
print(f"Cutoff 5 count: {c5_count}")
print(f"Bigger than 24 count: {big_count}")
