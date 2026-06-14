#!/bin/bash
#SBATCH --licenses=common
#SBATCH --time=120:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=nfrib
#SBATCH --error=./nf_rib.%J.err
#SBATCH --output=./nf_rib.%J.out

conda init bash
source ~/.bashrc
conda activate nfold_env

python /home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/canonize_chem_map_preds/fix_neuralfold_ribo.py

cd /mnt/nrdstor/yesselmanlab/ewhiting/neuralfold_scripts

for ff in $(cat /home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/canonize_chem_map_preds/fastas_todo.txt); do
    python ../Neuralfold/NEURALfold.py test /scratch/neuralfold/$ff > /work/yesselmanlab/ewhiting/outputs/ribonanza/$ff.dbn
done
