#!/bin/bash
#SBATCH --time=168:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=spt_rib
#SBATCH --partition=gpu
#SBATCH --gres=gpu
#SBATCH --error=./spt_rib.%J.err
#SBATCH --output=./spt_rib.%J.out

echo STARTING

python /home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/canonize_chem_map_preds/finish_spot_ribo.py

cd /mnt/nrdstor/yesselmanlab/ewhiting/SPOT-RNA

for ff in $(cat /mnt/nrdstor/yesselmanlab/ewhiting/spot_scripts/ribonanza/fastas_todo.txt); do
        python SPOT-RNA.py --inputs /scratch/$ff --outputs '/mnt/nrdstor/yesselmanlab/ewhiting/spot_scripts/ribonanza' --gpu 0;
done

rm /mnt/nrdstor/yesselmanlab/ewhiting/spot_scripts/ribonanza/*bpseq
rm /mnt/nrdstor/yesselmanlab/ewhiting/spot_scripts/ribonanza/*prob

echo "Done!"
