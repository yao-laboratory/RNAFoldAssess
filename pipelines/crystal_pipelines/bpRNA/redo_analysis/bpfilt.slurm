#!/bin/bash
#SBATCH --licenses=common
#SBATCH --time=60:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=bpfilt
#SBATCH --error=/home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/crystal_pipelines/bpRNA/redo_analysis/bpfilt.%J.err
#SBATCH --output=/home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/crystal_pipelines/bpRNA/redo_analysis/bpfilt.%J.out

conda init bash
source ~/.bashrc
module load java
conda activate rna_fold_assess

cd /home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/crystal_pipelines/bpRNA/redo_analysis
python filter_predictions.py

