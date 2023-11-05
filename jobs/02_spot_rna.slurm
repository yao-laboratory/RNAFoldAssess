#!/bin/bash
#SBATCH --licenses=common
#SBATCH --time=60:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=spot02
#SBATCH --error=/home/yesselmanlab/ewhiting/RNAFoldAssess/jobs/jspot02.%J.err
#SBATCH --output=/home/yesselmanlab/ewhiting/RNAFoldAssess/jobs/jspot02.%J.out


bash /home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/spot_rna_dms_pipeline/02_generate_predictions.sh
