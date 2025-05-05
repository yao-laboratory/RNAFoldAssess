#!/bin/bash
#SBATCH --licenses=common
#SBATCH --time=9:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=128GB
#SBATCH --job-name=edmfe
#SBATCH --error=edmfe.%J.err
#SBATCH --output=edmfe.%J.out

conda init bash
source ~/.bashrc

 python /home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/ens_def_analyses/align_preds_with_ens_def.py
