#!/bin/bash
#SBATCH --licenses=common
#SBATCH --time=36:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=context_dms_pipeline
#SBATCH --error=/home/yesselmanlab/ewhiting/RNAFoldAssess/jobs/jcontext_dms.%J.err
#SBATCH --output=/home/yesselmanlab/ewhiting/RNAFoldAssess/jobs/jcontext_dms.%J.out

conda init bash
source ~/.bashrc
conda activate rna_fold_assess
module load java

cd $HOME/RNAFoldAssess
python pipelines/contextfold_dms_pipeline.py
