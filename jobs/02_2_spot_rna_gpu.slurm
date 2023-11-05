#!/bin/bash
#SBATCH --licenses=common
#SBATCH --partition=yaolab
#SBATCH --time=60:00:00          # Run time in hh:mm:ss
#SBATCH --gres=gpu
#SBATCH --mem=64GB
#SBATCH --job-name=gpu_spot02
#SBATCH --error=/home/yesselmanlab/ewhiting/RNAFoldAssess/jobs/gjspot02.%J.err
#SBATCH --output=/home/yesselmanlab/ewhiting/RNAFoldAssess/jobs/gjspot02.%J.out


bash /home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/spot_rna_dms_pipeline/02_2_generate_predictions_gpu.sh

