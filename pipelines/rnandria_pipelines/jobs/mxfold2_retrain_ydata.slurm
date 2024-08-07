#!/bin/bash
#SBATCH --licenses=common
#SBATCH --time=72:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=mx2ry_and
#SBATCH --error=mx2ry_and.%J.err
#SBATCH --output=mx2ry_and.%J.out

conda init bash
source ~/.bashrc
conda activate rna_fold_assess
module load java

cd /home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/rnandria_pipelines/
python mxfold2_retrained_ydata.py
