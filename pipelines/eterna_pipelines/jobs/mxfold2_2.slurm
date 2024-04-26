#!/bin/bash
#SBATCH --licenses=common
#SBATCH --time=60:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=mx2_et
#SBATCH --error=/home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/eterna_pipelines/jobs/mx_2et.%J.err
#SBATCH --output=/home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/eterna_pipelines/jobs/mx_2et.%J.out

conda init bash
source ~/.bashrc
conda activate rna_fold_assess
module load java

cd /home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/eterna_pipelines/
python mxfold2_eterna_pipeline.py --partition=2

