#!/bin/bash
#SBATCH --licenses=common
#SBATCH --time=24:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=rna_fold_dms_pipeline
#SBATCH --error=/home/yesselmanlab/ewhiting/RNAFoldAssess/jobs/jrnafold_dms.%J.err
#SBATCH --output=/home/yesselmanlab/ewhiting/RNAFoldAssess/jobs/jrnafold_dms.%J.out

conda init bash
source ~/.bashrc
conda activate rna_fold_assess
module load java

cd $HOME/RNAFoldAssess
python pipelines/rnafold_dms_pipeline.py
