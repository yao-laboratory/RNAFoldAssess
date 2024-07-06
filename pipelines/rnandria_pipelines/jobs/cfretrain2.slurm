#!/bin/bash
#SBATCH --licenses=common
#SBATCH --time=60:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=cfr2_and
#SBATCH --error=/home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/rnandria_pipelines/cfr2_and.%J.err
#SBATCH --output=/home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/rnandria_pipelines/cfr2_and.%J.out

conda init bash
source ~/.bashrc
conda activate rna_fold_assess
module load java

cd /home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/rnandria_pipelines/
python cfretrain2.py
