import sys, os


script_name = sys.argv[1]
short_name = script_name[:3]

if not os.path.exists(f"jobs/{script_name}"):
    os.mkdir(f"jobs/{script_name}")

for partition in range(103):
    with open(f"jobs/{script_name}/{script_name}_{partition}.slurm", "w") as f:
        jobstr = f"""#!/bin/bash
#SBATCH --licenses=common
#SBATCH --time=24:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=64GB
#SBATCH --job-name=bp_{short_name}_{partition}
#SBATCH --error=./bp_{short_name}_{partition}.%J.err
#SBATCH --output=./bp_{short_name}_{partition}.%J.out

conda init bash
source ~/.bashrc
conda activate nfold_env
module load java

cd /home/yesselmanlab/ewhiting/RNAFoldAssess/pipelines/bprna_redo
python {script_name}.py {partition}
"""
        f.write(jobstr)
