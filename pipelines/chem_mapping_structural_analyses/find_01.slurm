#!/bin/bash
#SBATCH --time=72:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=cm_mot
#SBATCH --error=cm_mot.%J.err
#SBATCH --output=cm_mot.%J.out

conda init bash
source ~/.bashrc
conda activate rna_fold_assess

cd /home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/chem_mapping_structural_analyses
python 01_find_predicted_motifs.py
