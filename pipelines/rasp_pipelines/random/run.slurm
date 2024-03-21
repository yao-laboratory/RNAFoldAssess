#!/bin/bash
#SBATCH --licenses=common
#SBATCH --time=60:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=rn_rasp
#SBATCH --error=/home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/rasp_pipelines/random/rn_rasp.%J.err
#SBATCH --output=/home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/rasp_pipelines/random/rn_rasp.%J.out

conda init bash
source ~/.bashrc
conda activate rna_fold_assess
module load java

cd /home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/rasp_pipelines/random
python generate_for_all_species.py
rm *.seq
