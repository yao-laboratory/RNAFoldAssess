import os

from RNAFoldAssess.models import DataPoint
from RNAFoldAssess.models.scorers import EternaScorer


base_dir = "/common/yesselmanlab/ewhiting/ss_deeplearning_data/data"
# base_dir = /scratch/ss_deeplearning_data/data
C014G_json_file = f"{base_dir}/C014G.json"


def create_ranked_sample_list(sequence, reactivities, fasta_path, sample_destination="/scratch/sample/ss_file.txt", nsamples=10000):
    sample_path = "/home/yesselmanlab/ewhiting/EternaFold/src/contrafold"
    cmd = f"{sample_path} sample {fasta_path} --nsamples {nsamples} > {sample_destination}"
    os.system(cmd)
    f = open(sample_destination)
    data = [d.strip() for d in f.readlines()]
    f.close()
    data = set(data) # remove redundant structures
    structure_scores = []
    for structure in data:
        score = EternaScorer.score(sequence, structure, reactivities, DMS=True)
        structure_scores.append((structure, score))

    return sorted(structure_scores, key=lambda x: x[1], reverse=True)

print("Loading datapoints")
datapoints = DataPoint.factory(C014G_json_file, "C014G")

# for testing
print("Prepping first datapoint")
dp1 = datapoints[0]
fasta_file = open(f"{dp1.name}.fasta", "w")
fasta_file.write(dp1.to_fasta_string())
fasta_file.close()
print("Creating samples")
samples = create_ranked_sample_list(dp1.sequence, dp1.reactivities, f"{dp1.name}.fasta", f"{dp1.name}_samples_raw")
f = open(f"{dp1.name}_samples", "w")
print("Writing samples")
for sample in samples:
    line = f"{sample[0]} {sample[1]}\n"
    f.write(line)
f.close()
