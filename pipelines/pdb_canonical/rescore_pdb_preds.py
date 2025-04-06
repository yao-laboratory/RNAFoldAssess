from RNAFoldAssess.models.scorers import CanonicalBasePairScorer


wrong_report_file_path = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions/pdb_matched_set.txt"
new_report_path = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions"
models = [
    "ContextFold",
    "ContraFold",
    "EternaFold",
    "IPKnot",
    "MXFold",
    "MXFold2",
    "Neuralfold",
    "NUPACK",
    "pKnots",
    "RNAFold",
    "RNAStructure",
    "Simfold"
    "SPOT-RNA"
]

with open(wrong_report_file_path) as fh:
    data = [line.split(", ") for line in fh.readlines()]


model_index = 0
dp_index = 1
seq_index = 2
true_structure_index = 3
prediction_index = 4

for lenience in [0, 1]:
    with open(f"{new_report_path}/pdb_canonical_matched_{lenience}.txt", "w") as fh:
        for d in data:
            model_name = d[model_index]
            dp_name = d[dp_index]
            seq = d[seq_index]
            stc = d[true_structure_index]
            pred = d[prediction_index]
            new_line = f"{model_name}, {dp_name}, {seq}, {stc}, {pred}, "
            scorer = CanonicalBasePairScorer(seq, stc, pred, lenience)
            scorer.evaluate()
            s = scorer.sensitivity
            p = scorer.ppv
            f1 = scorer.f1
            new_line += f"{s}, {p}, {f1}\n"

            fh.write(new_line)


