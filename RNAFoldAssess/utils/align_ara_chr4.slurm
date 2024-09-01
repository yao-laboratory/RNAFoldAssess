#!/bin/bash
#SBATCH --licenses=common
#SBATCH --time=60:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=al_ara4
#SBATCH --error=al_ara4.%J.err
#SBATCH --output=al_ara4.%J.out

conda init bash
source ~/.bashrc

cd /home/yesselmanlab/ewhiting/RNAFoldAssess/RNAFoldAssess/utils
python aligning_ara_rasp_data_by_chromosome.py 4
