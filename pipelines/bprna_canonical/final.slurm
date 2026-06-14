#!/bin/bash
#SBATCH --time=72:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=bpcnf
#SBATCH --error=bpcnf.%J.err
#SBATCH --output=bpcnf.%J.out

conda init bash
source ~/.bashrc
conda activate rna_fold_assess

cd /home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/bprna_canonical/
python final_canonize.py
