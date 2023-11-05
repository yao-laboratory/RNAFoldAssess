#!/bin/bash
#SBATCH --licenses=common
#SBATCH --time=24:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=mxfold_dms_pipeline
#SBATCH --error=/home/yesselmanlab/ewhiting/RNAFoldAssess/jobs/jmxfold_dms.%J.err
#SBATCH --output=/home/yesselmanlab/ewhiting/RNAFoldAssess/jobs/jmxfold_dms.%J.out

conda init bash
source ~/.bashrc
conda activate rna_fold_assess

cd $HOME/RNAFoldAssess
python pipelines/mxfold_dms_pipeline.py
