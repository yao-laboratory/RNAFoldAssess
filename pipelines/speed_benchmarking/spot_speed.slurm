#!/bin/bash
#SBATCH --licenses=common
#SBATCH --time=168:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=spt_speed
#SBATCH --partition=gpu
#SBATCH --gres=gpu
#SBATCH --error=./spt_speed.%J.err
#SBATCH --output=./spt_speed.%J.out

conda activate spot_env
echo ABC
echo $DEFAULT_CONDA_ENV
echo DEF
cd /common/yesselmanlab/ewhiting/SPOT-RNA

echo copying files
cp /work/yesselmanlab/ewhiting/data/bprna/speed_dataset_fasta/* /scratch

echo starting evaluation

script_start=`date +%s`

for ff in $(ls /scratch); do
    python SPOT-RNA.py --inputs /scratch/$ff --outputs '../spot_outputs/' --gpu 0
done

script_end=`date +%s`

elapsed=$(bc -l <<< "$script_stop - $script_start")

touch /home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/speed_benchmarking/SPOT-RNA_speed_test.txt
echo $elapsed > /home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/speed_benchmarking/SPOT-RNA_speed_test.txt
