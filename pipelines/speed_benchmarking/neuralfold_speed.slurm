#!/bin/bash
#SBATCH --licenses=common
#SBATCH --time=72:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=nfes
#SBATCH --error=./nfes.%J.err
#SBATCH --output=./nfes.%J.out


conda init bash
source ~/.bashrc
conda activate nfold_env

cd /common/yesselmanlab/ewhiting/neuralfold_scripts

start_time=$(date +%s)

echo copying files
cp /work/yesselmanlab/ewhiting/data/bprna/speed_dataset_fasta/* /scratch

echo starting evaluation

for ff in $(ls /scratch); do
	python ../Neuralfold/NEURALfold.py test /scratch/$ff
done


end_time=$(date +%s)
duration=$((end_time - start_time))

echo $duration
touch nf_speed.txt
echo "$duration" > nf_speed.txt

