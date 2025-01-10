import os

from rna_secstruct import SecStruct

base_report_dir = "/work/yesselmanlab/ewhiting/bprna_canonical_reports"

def normalize_structure(stc):
    stc = list(stc)
    for i in range(len(stc)):
        if stc[i] in "[]{}<>":
            stc[i] = "."
    return "".join(stc)

# bpRNA_CRW_696 has a HAIRPIN-GGCCCUUGUGGUGC-(............) that is never predicted
# bpRNA_CRW_3832 has a JUNCTION-GAAU&GGAA-(..(&)..) that is never predicted
# bpRNA_CRW_10052 has a HELIX-AUCGCGGA&GCCGCGGU-((((((((&)))))))) that is never predicted

datapoints = {
    "bpRNA_CRW_696": "HAIRPIN-GGCCCUUGUGGUGC-(............)",
    "bpRNA_CRW_3832": "JUNCTION-GAAU&GGAA-(..(&)..)",
    "bpRNA_CRW_10052": "HELIX-AUCGCGGA&GCCGCGGU-((((((((&))))))))"
}

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

dp_model_map = {}
for dp in datapoints:
    dp_model_map[dp] = {
        "sequence": "",
        "structure": "",
        "motif": datapoints[dp],
        "predictions": {}
    }
    for m in models:
        dp_model_map[dp]["predictions"][m] = ""

for m in models:
    with open(f"{base_report_dir}/{m}_master_0_lenience.txt") as fh:
        preds = fh.readlines()
    preds.pop(0)
    preds = [p.split(", ") for p in preds]
    for dp in datapoints:
        for line in preds:
            if line[1] == dp:
                seq = line[3].upper()
                stc = line[4]
                pred = line[5]
                dp_model_map[dp]["sequence"] = seq
                dp_model_map[dp]["structure"] = stc
                dp_model_map[dp]["predictions"][m] = pred


for dp, data in dp_model_map.items():
    seq = data["sequence"]
    real_stc = data["structure"]
    motif_of_interest = data["motif"]
    real_motifs = SecStruct(seq, real_stc)
    for k, v in real_motifs.motifs.items():
        if len(v.sequence) <= 3:
            # Skipping short sequence motifs
            continue
        key = v.sequence + "-" + v.structure + "-" + v.m_type
        if key == motif_of_interest:
            motif = v
            break
    breakpoint()
    print(motif)