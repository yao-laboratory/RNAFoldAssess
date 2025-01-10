import os

from RNAFoldAssess.models.scorers import CanonicalBasePairScorer


wrong_report_path = "/work/yesselmanlab/ewhiting/redo_reports"
new_report_path = "/work/yesselmanlab/ewhiting/bprna_canonical_reports"

fname_format = "MODELNAME_master_LENIENCE_lenience.txt"

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
    "Simfold"
    # Need to do SPOT-RNA separately
]

headers = "model_name, dp_name, lenience, sequence, true_structure, predicted_structure, sensitivity, ppv, f1\n"

seq_index = 3
tru_index = 4
pred_index = 5

for model in models:
    print(f"Working {model}")
    for lenience in [0, 1]:
        fname = fname_format.replace("MODELNAME", model).replace("LENIENCE", str(lenience))
        with open(f"{wrong_report_path}/{fname}") as fh:
            data = fh.readlines()
        
        if not data[0].startswith(model):
            data.pop(0)
        
        data = [d.split(", ") for d in data]

        with open(f"{new_report_path}/{fname}", "w") as fh:
            fh.write(headers)
            for d in data:
                model_name = d[0]
                dp_name = d[1]
                new_line = f"{model_name}, {dp_name}, {lenience}, "
                # lenience_name = d[2]
                seq = d[seq_index]
                stc = d[tru_index]
                pred = d[pred_index]
                new_line += f"{seq}, {stc}, {pred}, "
                scorer = CanonicalBasePairScorer(seq, stc, pred, lenience)
                scorer.evaluate()
                s = scorer.sensitivity
                p = scorer.ppv
                f1 = scorer.f1
                new_line += f"{s}, {p}, {f1}\n"

                fh.write(new_line)


