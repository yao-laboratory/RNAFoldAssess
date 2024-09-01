#!/bin/bash
#SBATCH --licenses=common
#SBATCH --time=168:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=align_arab
#SBATCH --error=align_arab.%J.err
#SBATCH --output=align_arab.%J.out

conda init bash
source ~/.bashrc

cd /home/yesselmanlab/ewhiting/RNAFoldAssess/RNAFoldAssess/utils
python aligning_ara_rasp_data3.py
