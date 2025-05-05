#!/bin/bash
#SBATCH --licenses=common
#SBATCH --time=124:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=ef_h
#SBATCH --error=./ef_h.%J.err
#SBATCH --output=./ef_h.%J.out

conda init bash
source ~/.bashrc
module load java
conda activate rna_fold_assess

cd /home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/rasp_with_exons/human
python eternafold_preds.py 

