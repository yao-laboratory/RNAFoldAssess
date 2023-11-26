#!/bin/bash
#SBATCH --licenses=common
#SBATCH --time=48:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=ebpjob
#SBATCH --error=/home/yesselmanlab/ewhiting/RNAFoldAssess/jobs/ebpjob.%J.err
#SBATCH --output=/home/yesselmanlab/ewhiting/RNAFoldAssess/jobs/ebpjob.%J.out

conda init bash
source ~/.bashrc
conda activate rna_fold_assess

cd $HOME/RNAFoldAssess/pipelines/crystal_pipelines/bpRNA/
python eternafold_bpRNA.py
