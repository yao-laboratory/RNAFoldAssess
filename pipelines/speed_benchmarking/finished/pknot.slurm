#!/bin/bash
#SBATCH --time=48:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=pk_s
#SBATCH --error=./pk_s.%J.err
#SBATCH --output=./pk_s.%J.out

conda init bash
source ~/.bashrc
module load java
conda activate rna_fold_assess

cd /home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/speed_benchmarking
python pknot.py
