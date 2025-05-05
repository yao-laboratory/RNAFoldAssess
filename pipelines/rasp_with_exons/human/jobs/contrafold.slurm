#!/bin/bash
#SBATCH --licenses=common
#SBATCH --time=124:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=cfx_h
#SBATCH --error=./cfx_h.%J.err
#SBATCH --output=./cfx_h.%J.out

conda init bash
source ~/.bashrc
module load java
conda activate rna_fold_assess

cd /home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/rasp_with_exons/human
python contrafold_preds.py 

