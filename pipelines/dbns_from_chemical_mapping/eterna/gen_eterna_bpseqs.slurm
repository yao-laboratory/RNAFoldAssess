#!/bin/bash
#SBATCH --licenses=common
#SBATCH --time=60:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=ebpseq
#SBATCH --error=ebpseq.%J.err
#SBATCH --output=ebpseq.%J.out

conda init bash
source ~/.bashrc
conda activate rna_fold_assess
module load rnastructure
export DATAPATH=/util/opt/anaconda/deployed-conda-envs/packages/rnastructure/envs/rnastructure-6.1/share/rnastructure/data_tables


cd /home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/dbns_from_chemical_mapping/eterna/
python make_eterna_bpseqs.py
