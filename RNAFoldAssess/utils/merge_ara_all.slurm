#!/bin/bash
#SBATCH --licenses=common
#SBATCH --time=120:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=mg_ara_all
#SBATCH --error=mg_ara_all.%J.err
#SBATCH --output=mg_ara_all.%J.out

conda init bash
source ~/.bashrc

cd /home/yesselmanlab/ewhiting/RNAFoldAssess/RNAFoldAssess/utils
python merge_datapoints_ara_all.py
