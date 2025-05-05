#!/bin/bash
#SBATCH --licenses=common
#SBATCH --time=100:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=nuh19
#SBATCH --error=./nuh19.%J.err
#SBATCH --output=./nuh19.%J.out

conda init bash
source ~/.bashrc
module load java
conda activate rna_fold_assess

cd /home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/rasp_with_exons/human
python NUPACK_preds19.py 

