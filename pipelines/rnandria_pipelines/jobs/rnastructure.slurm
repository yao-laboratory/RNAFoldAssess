#!/bin/bash
#SBATCH --licenses=common
#SBATCH --time=60:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=rs_andria
#SBATCH --error=/home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/rnandria_pipelines/jobs/rs_andria.%J.err
#SBATCH --output=/home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/rnandria_pipelines/jobs/rs_andria.%J.out

conda init bash
source ~/.bashrc
conda activate rna_fold_assess
module load rnastructure

cd /home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/rnandria_pipelines/
python rnastructure.py
