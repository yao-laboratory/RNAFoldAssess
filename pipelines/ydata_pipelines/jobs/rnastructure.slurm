#!/bin/bash
#SBATCH --licenses=common
#SBATCH --time=60:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=rs_yd
#SBATCH --error=/home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/ydata_pipelines/jobs/rs_yd.%J.err
#SBATCH --output=/home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/ydata_pipelines/jobs/rs_yd.%J.out

conda init bash
source ~/.bashrc
conda activate rna_fold_assess
module load rnastructure
module load java
export DATAPATH=/util/opt/anaconda/deployed-conda-envs/packages/rnastructure/envs/rnastructure-6.1/share/rnastructure/data_tables

cd /home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/ydata_pipelines/
python generate_rnastructure.py
