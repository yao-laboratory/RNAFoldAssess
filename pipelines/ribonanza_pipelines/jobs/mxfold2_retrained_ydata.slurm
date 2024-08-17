#!/bin/bash
#SBATCH --licenses=common
#SBATCH --time=96:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=mxry_ribo
#SBATCH --error=mxry_ribo.%J.err
#SBATCH --output=mxry_ribo.%J.out

conda init bash
source ~/.bashrc
conda activate rna_fold_assess
module load java

cd /home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/ribonanza_pipelines/
python mxfold2_retrained_ydata.py