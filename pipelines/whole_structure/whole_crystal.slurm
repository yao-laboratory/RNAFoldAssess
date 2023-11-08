#!/bin/bash
#SBATCH --licenses=common
#SBATCH --time=36:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=eterna_dms_pipeline
#SBATCH --error=/home/yesselmanlab/ewhiting/RNAFoldAssess/jobs/whole.%J.err
#SBATCH --output=/home/yesselmanlab/ewhiting/RNAFoldAssess/jobs/whole.%J.out


conda activate rna_fold_assess
dir=/work/yesselmanlab/ewhiting/whole_structures

for f in $(ls $dir | grep py); do
	python $dir/$f
done

