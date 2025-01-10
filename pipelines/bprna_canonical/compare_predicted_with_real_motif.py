import json


base_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions"
json_path = f"{base_dir}/bprna_motif_prediction_data_trimmed.json"

models = [
    "ContextFold",
    "ContraFold",
    "EternaFold",
    "IPKnot",
    "MXFold",
    "MXFold2",
    "NeuralFold",
    "NUPACK",
    "pKnots",
    "RNAFold",
    "RNAStructure",
    "Simfold",
    "SPOT-RNA"
]

print("Loading data")
with open(json_path) as fh:
    data = json.load(fh)

dp_motif_of_interest = {
    "bpRNA_RFAM_41799": "JUNCTION_UCGUAGG&CUUGAACC_(.....(&)......)",
    "bpRNA_RFAM_1073": "SINGLESTRAND_AAGUAUAUUAAUCUGAUUUUUGGAUGAUC_.............................",
    "bpRNA_RFAM_14627": "HAIRPIN_GGAUUUUGAAAAGGU_(.............)",
    "bpRNA_RFAM_28128": "HAIRPIN_GUUCCCUCGGACGC_(............)",
    "bpRNA_RFAM_28236": "HAIRPIN_UUUUGCUCUAAGUA_(............)",
    "bpRNA_RFAM_649": "JUNCTION_CUAUAU&AG&UG_(....(&)(&))",
    "bpRNA_RFAM_18687": "HELIX_GUUCA&CGAAU_(((((&)))))"
}

for dp, motif in dp_motif_of_interest.items():
    real_motif = motif.split("_")[-1]
    relevant_seq = motif.split("_")[1]
    split_indexes = [i for i, char in enumerate(real_motif) if char == "&"]
    real_motif = real_motif.replace("&", " ")
    relevant_seq = relevant_seq.replace("&", " ")
    sequence = data[dp]["sequence"]
    if len(sequence) > 200:
        print(f"Skipping {dp} for length ({len(sequence)} nts)")
    structure = data[dp]["structure"]
    positions = data[dp]["motifs"][motif]["positions"]
    print(f"In {dp}, for motif {motif}")
    print(f"Positions: {positions}\n")
    for m in models:
        success = data[dp]["motifs"][motif][m]["success"]
        if not success:
            prediction = data[dp]["motifs"][motif][m]["prediction"]
            if len(split_indexes) > 0:
                prediction = list(prediction)
                for si in split_indexes:
                    prediction.insert(si, " ")
                prediction = "".join(prediction)
            print(f"{m} ->")
            print(f"\tMotif sequence:\t\t{relevant_seq}")
            print(f"\tMotif structure:\t{real_motif}")
            print(f"\tPrediction:\t\t{prediction}")
            print(f"\tMotif sequence:\t\t{relevant_seq}")
        else:
            print(f"Correctly predicted by {m}")
    print("\n")
