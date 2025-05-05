#!/bin/bash
#SBATCH --licenses=common
#SBATCH --time=72:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=mgh6
#SBATCH --error=mgh6.%J.err
#SBATCH --output=mgh6.%J.out

cd /home/yesselmanlab/ewhiting/RNAFoldAssess/RNAFoldAssess/utils
python create_master_coord_file_rasp_hum.py chr6
