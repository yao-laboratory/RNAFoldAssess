#!/bin/bash
#SBATCH --licenses=common
#SBATCH --time=60:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=mx2_yv
#SBATCH --error=/home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/ydata_pipelines/mx2_yv.%J.err
#SBATCH --output=/home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/ydata_pipelines/mx2_yv.%J.out

conda init bash
source ~/.bashrc
conda activate rna_fold_assess
module load java

cd /home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/ydata_pipelines
python generate_mxfold2_retrained_ribo.py C014V
