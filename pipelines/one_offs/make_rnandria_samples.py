import os

from RNAFoldAssess.models import DataPoint
from RNAFoldAssess.utils import ChemicalMappingTools, SecondaryStructureTools


base_path = "/common/yesselmanlab/ewhiting/data/rnandria/rnandria_data_JSON/processed"
pri_miRNA_path = f"{base_path}/pri_miRNA_datapoints.json"
human_mRNA_path = f"{base_path}/human_mRNA_datapoints.json"

p_dps = DataPoint.factory(pri_miRNA_path)
for dp in p_dps:
    ChemicalMappingTools.generate_from_datapoint(
        dp,
        "DMS",
        cf_loc=None,
        destination="/work/yesselmanlab/ewhiting/chem_map_to_bpseq/rnandria/bpseq_files/pri_miRNA"
    )

h_dps = DataPoint.factory(human_mRNA_path)
for dp in h_dps:
    ChemicalMappingTools.generate_from_datapoint(
        dp,
        "DMS",
        cf_loc=None,
        destination="/work/yesselmanlab/ewhiting/chem_map_to_bpseq/rnandria/bpseq_files/human_mRNA"
    )

