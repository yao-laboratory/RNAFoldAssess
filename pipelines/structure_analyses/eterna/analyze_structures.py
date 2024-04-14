from rna_secstruct import SecStruct


dataset_name = "EternaData"
data_dir = "/common/yesselmanlab/ewhiting/reports/eterna_data/ranked"

destination_dir = "/common/yesselmanlab/ewhiting/reports/eterna_data/motif_analysis"
problem_file = open(f"{destination_dir}/problem_file.txt", "w")

good_file = open(f"{data_dir}/EternaData_good_predictions.txt")
bad_file = open(f"{data_dir}/EternaData_bad_predictions.txt")

gdata = good_file.readlines()
bdata = bad_file.readlines()

good_file.close()
bad_file.close()

motif_and_count = {}
for d in bdata:
    d = d.split(", ")
    dp = d[1]
    seq = d[2]
    stc = d[3]
    if "[" in stc or "]" in stc:
        # There shouldn't be pseudoknots but
        # a few might have snuck through
        stc = stc.replace("[", ".").replace("]", ".")
        continue
    try:
        ss = SecStruct(seq, stc)
    except Exception as e:
        # This thing is touchy
        problem = f"Problem with {dp}. Exception: {e}"
        problem_file.write(problem)
        continue
    for k, v in ss.motifs.items():
        if len(v.sequence) <= 3:
            # Skipping short sequence motifs
            continue
        key = v.sequence + "_" + v.structure + "_" + v.m_type
        try:
            motif_and_count[key]["all_count"] += 1
            motif_and_count[key][f"bad_count"] += 1
            motif_and_count[key]["datapoint"].append(dp)
        except KeyError:
            motif_and_count[key] = {
                "all_count": 1,
                "bad_count": 1,
                "good_count": 0,
                "datapoint": [dp]
            }


print(f"Lengths after bdata: {len(motif_and_count)}")


for d in gdata:
    d = d.split(", ")
    dp = d[1]
    seq = d[2]
    stc = d[3]
    if "[" in stc or "]" in stc:
        # There shouldn't be pseudoknots but a few might have
        # snuck through
        stc = stc.replace("[", ".").replace("]", ".")
        continue
    try:
        ss = SecStruct(seq, stc)
    except Exception as e:
        # This thing is touchy
        problem = f"Problem with {dp}. Exception: {e}"
        problem_file.write(problem)
        continue
    for k, v in ss.motifs.items():
        if len(v.sequence) <= 3:
            # Skipping short sequence motifs
            continue
        key = v.sequence + "_" + v.structure + "_" + v.m_type
        try:
            motif_and_count[key]["all_count"] += 1
            motif_and_count[key][f"good_count"] += 1
            motif_and_count[key]["datapoint"].append(dp)
        except KeyError:
            motif_and_count[key] = {
                "all_count": 1,
                "bad_count": 0,
                "good_count": 1,
                "datapoint": [dp]
            }

print(f"Lengths after gdata: {len(motif_and_count)}")
problem_file.close()


# Filter out few-appearing motifs
relevant_motif_count = {}
cutoff = 10
for k in motif_and_count:
    d = motif_and_count[k]
    if d["all_count"] >= 10:
        relevant_motif_count[k] = d

print(f"Relevant motif count lenght: {len(relevant_motif_count)}")


only_in_good = []
only_in_bad = []

for k in relevant_motif_count:
    d = relevant_motif_count[k]
    if d["bad_count"] == 0:
        only_in_good.append(k)
    if d["good_count"] == 0:
        only_in_bad.append(k)


good_counts = []
bad_counts = []
good_only_counts = []
bad_only_counts = []

for k in relevant_motif_count:
    d = relevant_motif_count[k]
    gc = d["good_count"]
    bc = d["bad_count"]
    if gc > 0:
        good_counts.append((k, gc))
    else:
        bad_only_counts.append((k, bc))
    if bc > 0:
        bad_counts.append((k, bc))
    else:
        good_only_counts.append((k, gc))

good_counts = sorted(good_counts, key=lambda x: x[1], reverse=True)
bad_counts = sorted(bad_counts, key=lambda x: x[1], reverse=True)
good_only_counts = sorted(good_only_counts, key=lambda x: x[1], reverse=True)
bad_only_counts = sorted(bad_only_counts, key=lambda x: x[1], reverse=True)


good_prediction_motifs_file = open(f"{destination_dir}/{dataset_name}_motifs_only_in_good_predictions.txt", "w")
bad_prediction_motifs_file = open(f"{destination_dir}/{dataset_name}_motifs_only_in_bad_predictions.txt", "w")

for motif, count in good_only_counts:
    line = f"{motif}, {count}\n"
    good_prediction_motifs_file.write(line)

good_prediction_motifs_file.close()

for motif, count in bad_only_counts:
    line = f"{motif}, {count}\n"
    bad_prediction_motifs_file.write(line)

bad_prediction_motifs_file.close()
