import json

directory = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/rnandria/motifs"

with open(f"{directory}/canonical_motifs.json") as fh:
    datapoints = json.load(fh)

dp_pos_map = {}
print("Starting")
for dp, data in datapoints.items():
    sequence = data["sequence"]
    pos_map = {}
    for i in range(len(sequence)):
        pos_map[i] = {}

    models = data["models"]
    for m in models:
        motifs = models[m].items()
        for motif, positions in motifs:
            for p in positions:
                try:
                    pos_map[p][m].append([motif, positions])
                except KeyError:
                    pos_map[p][m] = [[motif, positions]]

    dp_pos_map[dp] = {}
    dp_pos_map[dp]["sequence"] = sequence
    dp_pos_map[dp]["positions"] = pos_map

print("Done")

with open(f"{directory}/rnandria_pos_map.json", "w") as fh:
    json.dump(dp_pos_map, fh)
