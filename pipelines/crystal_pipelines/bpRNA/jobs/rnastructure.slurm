#!/bin/bash
#SBATCH --licenses=common
#SBATCH --time=60:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=rs_bp
#SBATCH --error=/home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/crystal_pipelines/bpRNA/jobs/rs_bp.%J.err
#SBATCH --output=/home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/crystal_pipelines/bpRNA/jobs/rs_bp.%J.out

conda init bash
source ~/.bashrc
conda activate rna_fold_assess
module load rnastructure
module load java
export DATAPATH=/util/opt/anaconda/deployed-conda-envs/packages/rnastructure/envs/rnastructure-6.1/share/rnastructure/data_tables

cd /home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/crystal_pipelines/bpRNA/
python generate_rnastructure.py
