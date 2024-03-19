#!/bin/bash
#SBATCH --licenses=common
#SBATCH --time=60:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=et_eterna
#SBATCH --error=/home/yesselmanlab/ewhiting/RNAFoldAssess/jobs/et_eterna.%J.err
#SBATCH --output=/home/yesselmanlab/ewhiting/RNAFoldAssess/jobs/et_eterna.%J.out

conda init bash
module load java
source ~/.bashrc
conda activate rna_fold_assess

cd /home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/eterna_pipelines/
python eternafold_eterna_pipeline.py

