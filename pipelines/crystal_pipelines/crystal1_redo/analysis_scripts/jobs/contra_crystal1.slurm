#!/bin/bash
#SBATCH --licenses=common
#SBATCH --time=48:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=contra_c1
#SBATCH --error=/home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/crystal_pipelines/crystal1_redo/analysis_scripts/jobs/contra_c1.%J.err
#SBATCH --output=/home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/crystal_pipelines/crystal1_redo/analysis_scripts/jobs/contra_c1.%J.out

conda activate rna_fold_assess
module load java
python /home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/crystal_pipelines/crystal1_redo/analysis_scripts/contrafold_crystal1.py
