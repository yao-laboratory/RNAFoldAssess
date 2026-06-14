#!/bin/bash
#SBATCH --time=24:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=cnbp
#SBATCH --error=cnbp.%J.err
#SBATCH --output=cnbp.%J.out

conda init bash
source ~/.bashrc
conda activate rna_fold_assess

cd /home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/canonize_chem_map_preds/canonize_bprna
python canonize.py
