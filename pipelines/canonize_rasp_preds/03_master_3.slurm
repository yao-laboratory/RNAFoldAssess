#!/bin/bash
#SBATCH --time=60:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=rsc3
#SBATCH --error=rsc3.%J.err
#SBATCH --output=rsc3.%J.out

conda init bash
source ~/.bashrc
conda activate rna_fold_assess

cd /home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/canonize_rasp_preds
python 03_master_pred_file_split3.py
