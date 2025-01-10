#!/bin/bash
#SBATCH --licenses=common
#SBATCH --time=24:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=bp_canon
#SBATCH --error=./canon.%J.err
#SBATCH --output=./canon.%J.out

conda init bash
source ~/.bashrc
conda activate rna_fold_assess

cd /home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/bprna_canonical
python get_canonical_accuracies.py
