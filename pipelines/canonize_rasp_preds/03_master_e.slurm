#!/bin/bash
#SBATCH --time=72:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=mrspe
#SBATCH --error=mrspe.%J.err
#SBATCH --output=mrspe.%J.out

conda init bash
source ~/.bashrc
conda activate rna_fold_assess

cd /home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/canonize_rasp_preds
python 03_02_master_pred_file_ecoli.py
