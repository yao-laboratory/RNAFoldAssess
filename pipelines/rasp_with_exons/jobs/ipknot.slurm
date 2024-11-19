#!/bin/bash
#SBATCH --licenses=common
#SBATCH --time=24:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=ip_r
#SBATCH --error=ip_r.%J.err
#SBATCH --output=ip_r.%J.out

conda init bash
source ~/.bashrc
conda activate rna_fold_assess
module load java


cd /home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/rasp_with_exons
python ipknot_preds.py
