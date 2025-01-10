base_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions"


def parse_structure(structure):
    # structure exampe: "..((((...))))..((..))."
    bps = []
    for i1, c1 in enumerate(structure):
        if c1 != '(':
            continue
        count = 1
        for i2, c2 in enumerate(structure[i1 + 1:]):
            if c2 == '(':
                count += 1
            elif c2 == ')':
                count -= 1
                if count == 0:
                    bps.append((i1, i1 + i2 + 1))
                    break
    return bps


with open(f"{base_dir}/bprna_difficult_motifs.txt") as fh:
    data = fh.readlines()

woble_pairs = ["UG", "GU"]
woble_count = 0
no_woble_count = 0
stc_with_woble = 0
non_wobels = []

for d in data:
    mtype, seq, stc = d.split("_")
    seq = seq.replace("&", "")
    stc = stc.replace("&", "")
    base_pairs = parse_structure(stc)
    found_woble = False
    for x, y in base_pairs:
        bp = f"{seq[x]}{seq[y]}"
        if bp in woble_pairs:
            found_woble = True
            woble_count += 1
    if not found_woble:
        no_woble_count += 1
        non_wobels.append(d)
    else:
        stc_with_woble += 1

print(f"There are {woble_count:,} instance of woble pairs in {len(data):,} motifs")
print(f"There are {stc_with_woble:,} motifs in {len(data):,} with at least one wobel pair")
print(f"There are {no_woble_count:,} motifs in {len(data):,} with no wobel pairs")

with open(f"{base_dir}/bprna_difficult_motifs_no_wobel.txt", "w") as fh:
    for d in non_wobels:
        fh.write(d)
