#!/bin/bash
#SBATCH --licenses=common
#SBATCH --time=100:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=rs_h
#SBATCH --error=./rs_h.%J.err
#SBATCH --output=./rs_h.%J.out

conda init bash
source ~/.bashrc
module load java
conda activate rna_fold_assess
module load rnastructure
export DATAPATH=/util/opt/anaconda/deployed-conda-envs/packages/rnastructure/envs/rnastructure-6.1/share/rnastructure/data_tables

cd /home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/rasp_with_exons/human
python rnastructure_preds.py 

