#!/bin/bash
#SBATCH --licenses=common
#SBATCH --time=60:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=pk_r1
#SBATCH --error=pk_r1.%J.err
#SBATCH --output=pk_r1.%J.out

conda init bash
source ~/.bashrc
conda activate rna_fold_assess
module load java
module load viennarna

cd /home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/rasp_with_exons
python pknot_preds_ch1.py
