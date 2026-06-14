#!/bin/bash
#SBATCH --time=72:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=mrasp
#SBATCH --error=mrsph.%J.err
#SBATCH --output=mrsph.%J.out

conda init bash
source ~/.bashrc
conda activate rna_fold_assess

cd /home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/canonize_rasp_preds
python 03_01_master_pred_file_human.py
