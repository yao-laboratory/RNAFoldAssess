#!/bin/bash
#SBATCH --licenses=common
#SBATCH --time=36:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=bp_mtf2
#SBATCH --error=./bp_mtf2.%J.err
#SBATCH --output=./bp_mtf2.%J.out

conda init bash
source ~/.bashrc
conda activate rna_fold_assess

cd /home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/bprna_canonical/acug_only
python trim_motif_prediction_file.py
