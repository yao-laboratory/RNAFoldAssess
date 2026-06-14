#!/bin/bash
#SBATCH --time=72:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=nfes
#SBATCH --error=./nfes2.%J.err
#SBATCH --output=./nfes2.%J.out


conda init bash
source ~/.bashrc
conda activate nfold_env

cd /mnt/nrdstor/yesselmanlab/ewhiting/neuralfold_scripts

start_time=$(date +%s)

echo copying files
cp /work/yesselmanlab/ewhiting/data/bprna/speed_dataset_fasta/* /scratch

echo starting evaluation

for i in {1..10}; do
	for ff in $(ls /scratch); do
		python ../Neuralfold/NEURALfold.py test /scratch/$ff
	done


	end_time=$(date +%s)
	duration=$((end_time - start_time))

	echo $duration
	touch nf_speed_$i.txt
	echo "$duration" > nf_speed_$i.txt
done
