#!/bin/bash
#SBATCH --licenses=common
#SBATCH --time=60:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=mg_ara4
#SBATCH --error=mg_ara4.%J.err
#SBATCH --output=mg_ara4.%J.out

conda init bash
source ~/.bashrc

cd /home/yesselmanlab/ewhiting/RNAFoldAssess/RNAFoldAssess/utils
python merge_datapoints_ara_4.py
