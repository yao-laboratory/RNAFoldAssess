#!/bin/bash
#SBATCH --licenses=common
#SBATCH --time=168:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=mxre_ribo
#SBATCH --error=mxre_ribo.%J.err
#SBATCH --output=mxre_ribo.%J.out

conda init bash
source ~/.bashrc
conda activate rna_fold_assess
module load java

cd /home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/ribonanza_pipelines/
python mxfold2_retrained_eterna.py