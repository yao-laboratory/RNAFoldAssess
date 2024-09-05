#!/bin/bash
#SBATCH --licenses=common
#SBATCH --time=60:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=mg_araMt
#SBATCH --error=mg_araMt.%J.err
#SBATCH --output=mg_araMt.%J.out

conda init bash
source ~/.bashrc

cd /home/yesselmanlab/ewhiting/RNAFoldAssess/RNAFoldAssess/utils
python merge_datapoints_ara_Mt.py
