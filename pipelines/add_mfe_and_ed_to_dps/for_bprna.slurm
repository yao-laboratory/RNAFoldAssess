#!/bin/bash
#SBATCH --licenses=common
#SBATCH --time=120:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=an_bp
#SBATCH --error=an_bp.%J.err
#SBATCH --output=an_bp.%J.out

conda init bash
source ~/.bashrc
conda activate rnafa_backup
module load viennarna

cd /home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/add_mfe_and_ed_to_dps
python for_bprna.py
