import os


from RNAFoldAssess.models import DataPoint, EternaDataPoint, DataPointFromCrystal
from RNAFoldAssess.utils import ChemicalMappingTools, SecondaryStructureTools


def get_all_reactivities(datapoint):
    positions = datapoint.positions
    reactivities = datapoint.reactivities
    seq_size = len(datapoint.sequence)
    new_reactivities = []
    reactivities_pointer = 0
    for i in range(seq_size):
        if i in positions:
            new_reactivities.append(reactivities[reactivities_pointer])
            reactivities_pointer += 1
        else:
            new_reactivities.append(float(-999))
    return new_reactivities


if __name__ == "__main__":
    data_points_path="/common/yesselmanlab/ewhiting/data/translated_eterna_data/eterna.json"
    
    datapoints = EternaDataPoint.factory(data_points_path)
    bpseq_dest = "/work/yesselmanlab/ewhiting/chem_map_to_bpseq/eterna/bpseq_files"
    
    for dp in datapoints:
        try:
            dp.reactivities = get_all_reactivities(dp)
            if dp.mapping_method == "DMS":
                ss_file = ChemicalMappingTools.generate_from_datapoint(dp, "DMS")
            else:
                ss_file = ChemicalMappingTools.generate_from_datapoint(dp, "SHAPE")
            with open(ss_file) as sf:
                ss_data = sf.readlines()
            dbn = ss_data[2].strip()
            SecondaryStructureTools.write_bpseq_file(dp.name, dp.sequence, dbn, bpseq_dest)
            os.remove(ss_file)
        except:
            continue

