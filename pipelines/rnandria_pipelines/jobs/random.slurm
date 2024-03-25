#!/bin/bash
#SBATCH --licenses=common
#SBATCH --time=60:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=rn_and
#SBATCH --error=/home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/rnandria_pipelines/rn_and.%J.err
#SBATCH --output=/home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/rnandria_pipelines/rn_and.%J.out

conda init bash
source ~/.bashrc
conda activate rna_fold_assess
module load java

cd /home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/rnandria_pipelines/
python random_predictor.py
