from RNAFoldAssess.models.scorers import BasePairScorer


def to_fasta_scratch(name, sequence, path=""):
    fasta_string = f">{name}\n{sequence}\n"
    if path != "":
        path = f"/scratch/{path}"
    else:
        path = "/scratch"
    with open(f"{path}/{name}.fasta", "w") as f:
        f.write(fasta_string)
    return f"{path}/{name}.fasta"


def report_path(model_name, lenience, partition):
    base_path = "/work/yesselmanlab/ewhiting/bprna_preds/redo_reports"
    return f"{base_path}/{model_name}_{partition}_bpRNA_predictions_{lenience}_lenience.txt"


def pred_lines(true_structure, prediction, lenience):
    scorer = BasePairScorer(true_structure, prediction, lenience)
    scorer.evaluate()
    s = scorer.sensitivity
    p = scorer.ppv
    f1 = scorer.f1
    return f"{true_structure}, {prediction}, {s}, {p}, {f1}\n"


def get_seq_and_dbn(path):
    with open(path) as f:
        dbn_data = f.readlines()
    seq = dbn_data[3].strip()
    dbn = dbn_data[4].strip()
    if len(seq) != len(dbn):
        return False
    else:
        return (seq, dbn)
