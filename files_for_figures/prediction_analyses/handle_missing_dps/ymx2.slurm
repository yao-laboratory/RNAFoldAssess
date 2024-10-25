#!/bin/bash
#SBATCH --licenses=common
#SBATCH --time=60:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=mx2_et
#SBATCH --error=ymx2.%J.err
#SBATCH --output=ymx2.%J.out


conda init bash
source ~/.bashrc
conda activate rna_fold_assess

cd /home/yesselmanlab/ewhiting/RNAFoldAssess/files_for_figures/prediction_analyses/handle_missing_dps/
python ydata_mxfold2.py
