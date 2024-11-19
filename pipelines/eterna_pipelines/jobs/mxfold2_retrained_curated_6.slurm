#!/bin/bash
#SBATCH --licenses=common
#SBATCH --time=60:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=mx2rb6_et
#SBATCH --error=mx2c6_et.%J.err
#SBATCH --output=mx2c6_et.%J.out

conda init bash
source ~/.bashrc
conda activate rna_fold_assess
module load java

cd /home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/eterna_pipelines/
python mxfold2_retrained_curated.py --partition=6
