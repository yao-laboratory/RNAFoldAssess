#!/bin/bash
#SBATCH --licenses=common
#SBATCH --time=60:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=cfr2_rsp
#SBATCH --error=/home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/rasp_pipelines/cfretrain2/cfr2_rsp.%J.err
#SBATCH --output=/home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/rasp_pipelines/cfretrain2/cfr2_rsp.%J.out

conda init bash
source ~/.bashrc
conda activate rna_fold_assess
module load java

cd /home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/rasp_pipelines/cfretrain2
python generate_for_all_species.py
