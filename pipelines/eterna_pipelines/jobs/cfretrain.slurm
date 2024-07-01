#!/bin/bash
#SBATCH --licenses=common
#SBATCH --time=60:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=cfr_et
#SBATCH --error=/home/yesselmanlab/ewhiting/RNAFoldAssess/jobs/cfr_et.%J.err
#SBATCH --output=/home/yesselmanlab/ewhiting/RNAFoldAssess/jobs/cfr_et.%J.out

conda init bash
module load java
source ~/.bashrc
conda activate rna_fold_assess

cd /home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/eterna_pipelines/
python cfretrain_eterna_pipeline.py

