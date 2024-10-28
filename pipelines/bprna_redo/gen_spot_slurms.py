import os, sys



partition = sys.argv[1]
destination = "/work/yesselmanlab/ewhiting/spot_scripts/bprna"
fasta_path = f"/work/yesselmanlab/ewhiting/data/bprna/fastaFiles_sep/part_{partition}"

if not os.path.isdir(f"{destination}/part_{partition}"):
    os.mkdir(f"{destination}/part_{partition}")

slurm_string = f"""#!/bin/bash
#SBATCH --licenses=common
#SBATCH --time=72:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=sptbp_{partition}
#SBATCH --partition=gpu
#SBATCH --gres=gpu
#SBATCH --error=./sptbp_{partition}.%J.err
#SBATCH --output=./sptbp_{partition}.%J.out

conda activate spot_env
cd /common/yesselmanlab/ewhiting/SPOT-RNA

for dp in $(ls {fasta_path}); do
        python SPOT-RNA.py --inputs {fasta_path}/$dp --outputs '{destination}/part_{partition}' --gpu 0
done
echo "Removing prob and bpseq files"
rm {destination}/part_{partition}/*prob
rm {destination}/part_{partition}/*bpseq

echo "Done!"
"""

with open(f"{destination}/job_{partition}.slurm", "w") as fh:
    fh.write(slurm_string)
