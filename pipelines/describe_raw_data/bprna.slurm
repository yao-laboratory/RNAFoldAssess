#!/bin/bash
#SBATCH --licenses=common
#SBATCH --time=60:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=bpdes
#SBATCH --error=/home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/describe_raw_data/bpdes.%J.err
#SBATCH --output=/home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/describe_raw_data/bpdes.%J.out

cd /home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/describe_raw_data/
python bprna.py
