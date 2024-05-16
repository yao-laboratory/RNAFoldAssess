import os


from RNAFoldAssess.models import DataPoint


base_path = "/common/yesselmanlab/ewhiting/data/rnandria/rnandria_data_JSON/processed"
pri_miRNA = f"{base_path}/pri_miRNA_datapoints.json"
human_mRNA = f"{base_path}/human_mRNA_datapoints.json"

pri_destination = "/common/yesselmanlab/ewhiting/data/fasta_files/rnandria/pri_miRNA"
human_destination = "/common/yesselmanlab/ewhiting/data/fasta_files/rnandria/human_mRNA"

pri_dps = DataPoint.factory(pri_miRNA)
human_dps = DataPoint.factory(human_mRNA)

print("Starting on micro RNA data points")
for dp in pri_dps:
    with open(f"{pri_destination}/{dp.name}.fasta", "w") as f:
        f.write(dp.to_fasta_string())

print("Starting on messenger RNA data points")
for dp in human_dps:
    with open(f"{human_destination}/{dp.name}.fasta", "w") as f:
        f.write(dp.to_fasta_string())

print("Done")
