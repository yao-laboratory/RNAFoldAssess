import os, json, heapq

import rda_kit


class RDATPreprocessing:
  """
  A class for wrangling data in .rdat files
  """
  @staticmethod
  def get_constructs(path):
      rdat = rda_kit.RDATFile()
      rdat.load(open(path))
      constructs = list(rdat.constructs)
      experiments = rdat.annotations["modifier"]
      for c in constructs:
        construct = rdat.constructs[c]
        structure = c.structure
        handlers = c.data




# # Test
# path = "../../data/MTTR15_DMS_0001.rdat"

# info = RDATPreprocessing.rdat_to_json_record(path, True)
# print(info)
# # For this particular one, the first set of reactivities is the DMS data


# rdat_root = "/common/yesselmanlab/ewhiting/data/rmdb_data/good_rdats"
# file_of_rdats = f"{rdat_root}/rdats_with_dms.txt"
