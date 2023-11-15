#!/bin/bash
#SBATCH --licenses=common
#SBATCH --time=48:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=c2job
#SBATCH --error=/home/yesselmanlab/ewhiting/RNAFoldAssess/jobs/c2job.%J.err
#SBATCH --output=/home/yesselmanlab/ewhiting/RNAFoldAssess/jobs/c2job.%J.out

conda init bash
source ~/.bashrc
conda activate rna_fold_assess

cd $HOME/RNAFoldAssess/pipelines/crystal_pipelines/crystal2/
for f in $(ls | grep py); do
    python $f
done
