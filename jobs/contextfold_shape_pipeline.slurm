#!/bin/bash
#SBATCH --licenses=common
#SBATCH --time=24:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=cf_shape
#SBATCH --error=/home/yesselmanlab/ewhiting/RNAFoldAssess/jobs/cf_shape.%J.err
#SBATCH --output=/home/yesselmanlab/ewhiting/RNAFoldAssess/jobs/cf_shape.%J.out

conda init bash
source ~/.bashrc
conda activate rna_fold_assess

cd $HOME/RNAFoldAssess
python pipelines/SHAPE_pipelines/contextfold_shape_pipeline.py
