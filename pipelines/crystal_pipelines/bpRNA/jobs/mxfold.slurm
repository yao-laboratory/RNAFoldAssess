#!/bin/bash
#SBATCH --licenses=common
#SBATCH --time=60:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=mx_bp
#SBATCH --error=/home/yesselmanlab/ewhiting/RNAFoldAssess/jobs/mx_bp.%J.err
#SBATCH --output=/home/yesselmanlab/ewhiting/RNAFoldAssess/jobs/mx_bp.%J.out

conda init bash
source ~/.bashrc
module load java
conda activate rna_fold_assess

cd /home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/crystal_pipelines/bpRNA/
python generate_rna_fold_bpRNA.py

