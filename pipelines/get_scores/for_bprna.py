import os


models = ["ContextFold", "ContraFold", "EternaFold", "IPKnot",
          "NeuralFold", "NUPACK", "RNAFold",
          "RNAStructure", "pKnots", "Simfold",
          "MXFold", "MXFold2", "SPOT-RNA"]

base_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions"
dps_file =f"{base_dir}/all_bprna_datapoints.txt"
with open(dps_file) as fh:
    dps = [line.split(", ")[0] for line in fh.readlines()]

# Waiting for job:
# /home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/bprna_canonical/final.slurm
