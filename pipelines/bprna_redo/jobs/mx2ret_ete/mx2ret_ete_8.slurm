#!/bin/bash
#SBATCH --licenses=common
#SBATCH --time=24:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=bp_mx2_8
#SBATCH --error=./bp_mx2_8.%J.err
#SBATCH --output=./bp_mx2_8.%J.out

conda init bash
source ~/.bashrc
conda activate rna_fold_assess
module load java

cd /home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/bprna_redo
python mx2ret_ete.py 8
