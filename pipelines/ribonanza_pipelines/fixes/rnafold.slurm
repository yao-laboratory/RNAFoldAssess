#!/bin/bash
#SBATCH --licenses=common
#SBATCH --time=60:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=rf_ribo
#SBATCH --error=/home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/ribonanza_pipelines/fixes/rf_ribo.%J.err
#SBATCH --output=/home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/ribonanza_pipelines/fixes/rf_ribo.%J.out

conda init bash
source ~/.bashrc
conda activate rna_fold_assess
module load java
module load viennarna

cd /home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/ribonanza_pipelines/fixes
python rnafold_fix.py

