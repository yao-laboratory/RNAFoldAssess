#!/bin/bash
#SBATCH --time=168:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=scara
#SBATCH --error=scara.%J.err
#SBATCH --output=scara.%J.out

conda init bash
source ~/.bashrc
conda activate rna_fold_assess

cd /home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/canonize_rasp_preds
python 04_00_ara_scores.py
