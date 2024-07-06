#!/bin/bash
#SBATCH --licenses=common
#SBATCH --time=72:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=cfr2_rib
#SBATCH --error=./cfr2_rib.%J.err
#SBATCH --output=./cfr2_rib.%J.out

conda init bash
source ~/.bashrc
conda activate rna_fold_assess
module load java

cd /home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/ribonanza_pipelines/
python cfretrained2.py
rm *.seq
