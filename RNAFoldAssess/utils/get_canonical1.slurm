#!/bin/bash
#SBATCH --time=48:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=get_canonical
#SBATCH --error=/home/yesselmanlab/ewhiting/RNAFoldAssess/RNAFoldAssess/utils/test_pdb_tools.%J.err
#SBATCH --output=/home/yesselmanlab/ewhiting/RNAFoldAssess/RNAFoldAssess/utils/test_pdb_tools.%J.out

cd /home/yesselmanlab/ewhiting/RNAFoldAssess/RNAFoldAssess/utils && python test_pdb_tools.py
