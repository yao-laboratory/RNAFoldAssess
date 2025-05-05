#!/bin/bash
#SBATCH --licenses=common
#SBATCH --time=100:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=ip_h
#SBATCH --error=./ip_h.%J.err
#SBATCH --output=./ip_h.%J.out

conda init bash
source ~/.bashrc
module load java
conda activate rna_fold_assess

cd /home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/rasp_with_exons/human
python ipknot_preds.py 

