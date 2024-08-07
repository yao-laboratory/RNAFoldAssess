#!/bin/bash
#SBATCH --licenses=common
#SBATCH --time=60:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=rabpq
#SBATCH --error=rabpq.%J.err
#SBATCH --output=rabpq.%J.out

conda init bash
source ~/.bashrc
conda activate rna_fold_assess
module load rnastructure
export DATAPATH=/util/opt/anaconda/deployed-conda-envs/packages/rnastructure/envs/rnastructure-6.1/share/rnastructure/data_tables


cd /home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/one_offs
python make_rnandria_samples.py