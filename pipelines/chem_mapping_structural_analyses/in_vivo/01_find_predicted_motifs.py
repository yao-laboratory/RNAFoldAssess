import json

from rna_secstruct import SecStruct


def get_sec_struct_object(seq, stc):
    try:
        return SecStruct(seq, stc)
    except:
        return False


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

base_dir = ""
