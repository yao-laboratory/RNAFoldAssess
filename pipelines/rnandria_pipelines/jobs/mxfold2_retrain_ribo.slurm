#!/bin/bash
#SBATCH --licenses=common
#SBATCH --time=72:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=mx2rb_and
#SBATCH --error=mx2rb_and.%J.err
#SBATCH --output=mx2rb_and.%J.out

conda init bash
source ~/.bashrc
conda activate rna_fold_assess
module load java

cd /home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/rnandria_pipelines/
python mxfold2_retrained_ribonanza.py
