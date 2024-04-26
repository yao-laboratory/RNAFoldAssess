#!/bin/bash
#SBATCH --licenses=common
#SBATCH --time=72:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=mx2_rasp
#SBATCH --error=/home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/rasp_pipelines/mxfold2/mx2_rasp.%J.err
#SBATCH --output=/home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/rasp_pipelines/mxfold2/mx2_rasp.%J.out

conda init bash
source ~/.bashrc
conda activate rna_fold_assess
module load java

cd /home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/rasp_pipelines/mxfold2
python generate_for_all_species.py
