#!/bin/bash
#SBATCH --licenses=common
#SBATCH --time=60:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=rf_ribo
#SBATCH --error=rf_ribo.%J.err
#SBATCH --output=rf_ribo.%J.out

conda init bash
source ~/.bashrc
conda activate rna_fold_assess
module load viennarna
module load java

cd /home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/ribonanza_pipelines/
python rnafold.py

