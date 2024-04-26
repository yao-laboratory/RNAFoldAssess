#!/bin/bash
#SBATCH --licenses=common
#SBATCH --time=60:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=rs_eterna
#SBATCH --error=/home/yesselmanlab/ewhiting/RNAFoldAssess/jobs/rs_eterna.%J.err
#SBATCH --output=/home/yesselmanlab/ewhiting/RNAFoldAssess/jobs/rs_eterna.%J.out

conda init bash
source ~/.bashrc
conda activate rna_fold_assess
module load rnastructure

cd /home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/eterna_pipelines/
python rnastructure_eterna_pipeline.py

