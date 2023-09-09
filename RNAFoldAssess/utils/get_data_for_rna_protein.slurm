#!/bin/bash
#SBATCH --time=48:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=128GB
#SBATCH --job-name=rna_protein
#SBATCH --error=/home/yesselmanlab/ewhiting/RNAFoldAssess/RNAFoldAssess/utils/rna_protein.%J.err
#SBATCH --output=/home/yesselmanlab/ewhiting/RNAFoldAssess/RNAFoldAssess/utils/rna_protein.%J.out

cd /home/yesselmanlab/ewhiting/RNAFoldAssess/RNAFoldAssess/utils && python test_pdb_tools.py