#!/bin/bash
#SBATCH --licenses=common
#SBATCH --time=24:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=et_r
#SBATCH --error=et_r.%J.err
#SBATCH --output=et_r.%J.out

conda init bash
source ~/.bashrc
conda activate rna_fold_assess
module load java


cd /home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/rasp_with_exons
python eternafold_preds.py
