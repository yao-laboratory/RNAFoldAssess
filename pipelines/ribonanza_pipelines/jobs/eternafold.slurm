#!/bin/bash
#SBATCH --licenses=common
#SBATCH --time=60:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=e_ribo
#SBATCH --error=/home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/ribonanza_pipelines/e_ribo.%J.err
#SBATCH --output=/home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/ribonanza_pipelines/e_ribo.%J.out

conda init bash
source ~/.bashrc
conda activate rna_fold_assess
module load java

cd /home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/ribonanza_pipelines/
python eternafold.py
rm *.seq
