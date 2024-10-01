import os


from RNAFoldAssess.utils import ChemicalMappingTools, SecondaryStructureTools


base_path = "/work/yesselmanlab/ewhiting/chem_map_to_bpseq/rnandria"
pri_path = f"{base_path}/pri_miRNA"
hum_path = f"{base_path}/human_mRNA"

for dbn_file in os.listdir(pri_path):
    name = dbn_file.strip(".dbn")
    with open(f"{pri_path}/{dbn_file}") as f:
        data = f.readlines()
    seq = data[1].strip()
    dbn = data[2].strip()
    SecondaryStructureTools.write_bpseq_file(
        name,
        seq,
        dbn,
        "/work/yesselmanlab/ewhiting/chem_map_to_bpseq/rnandria/bpseq_files/pri_miRNA"
    )


for dbn_file in os.listdir(hum_path):
    name = dbn_file.strip(".dbn")
    with open(f"{hum_path}/{dbn_file}") as f:
        data = f.readlines()
    seq = data[1].strip()
    dbn = data[2].strip()
    SecondaryStructureTools.write_bpseq_file(
        name,
        seq,
        dbn,
        "/work/yesselmanlab/ewhiting/chem_map_to_bpseq/rnandria/bpseq_files/human_mRNA"
    )

