#!/bin/bash
#SBATCH --licenses=common
#SBATCH --time=24:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=rasp_ara
#SBATCH --error=/home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/rasp_pipelines/arabidopsis/rasp_ara.%J.err
#SBATCH --output=/home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/rasp_pipelines/arabidopsis/rasp_ara.%J.out

conda init bash
source ~/.bashrc
conda activate rna_fold_assess
module load java

/home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/rasp_pipelines/arabidopsis
python generate_mxfold.py
python evaluate_mxfold.py


