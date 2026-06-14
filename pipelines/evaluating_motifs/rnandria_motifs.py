import os, json

from rna_secstruct import SecStruct


def get_sec_struct_object(seq, stc):
    try:
        return SecStruct(seq, stc)
    except:
        return False


report_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/rnandria/canonical"
models = [
    "ContextFold",
    "ContraFold",
    "EternaFold",
    "IPKnot",
    "NeuralFold",
    "NUPACK",
    "RNAFold",
    "RNAStructure",
    "pKnots",
    "Simfold",
    "MXFold",
    "MXFold2",
    "SPOT-RNA"
]


model_dp_map = {}
for m in models:
    model_dp_map[m] = {}

print(f"Making model_dp_map")
for m in models:
    files = [f for f in os.listdir(report_dir) if f"{m}_" in f]
    lines = []
    for f in files:
        with open(f"{report_dir}/{f}") as fh:
            lines += fh.readlines()
    lines = [line.split(", ") for line in lines]
    for line in lines:
        dp = line[1]
        seq = line[2]
        pred = line[3]

        motif_data = get_sec_struct_object(seq, pred)
        if not motif_data:
            continue

        model_dp_map[m][dp] = {
            "sequence": seq,
            "motifs": {}
        }
        for k, v in motif_data.motifs.items():
            key = v.m_type + "_" + v.sequence + "_" + v.structure
            positions = v.positions
            model_dp_map[m][dp]["motifs"][key] = positions


print("Making dp_motif_map")
dp_motif_map = {}
for m in models:
    dps = list(model_dp_map[m].keys())
    for dp in dps:
        if dp not in dp_motif_map:
            seq = model_dp_map[m][dp]["sequence"]
            dp_motif_map[dp] = {"sequence": seq, "models": {}}
            for model in models:
                dp_motif_map[dp]["models"][model] = {}

        motifs_in_dp = model_dp_map[m][dp]["motifs"]
        for motif, positions in motifs_in_dp.items():
            dp_motif_map[dp]["models"][m][motif] = positions

print("Writing file")
dest_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/rnandria/motifs"
with open(f"{dest_dir}/canonical_motifs.json", "w") as fh:
    json.dump(dp_motif_map, fh)

print("Done")
