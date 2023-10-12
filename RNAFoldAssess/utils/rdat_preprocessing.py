import os, json, heapq


class RDATPreprocessing:
  """
  A class for transforming data from several .rdat files
  into JSON records formatted in the way the `DataPoint`
  factory method expects.
  """
  @staticmethod
  def rdat_to_json_record(path_to_rdat, normalize_reactivities=False):
    f = open(path_to_rdat)
    data = f.readlines()
    f.close()
    seq, struc, name = "", "", ""
    reactivities = {}
    for line in data:
      spl = line.split("\t")
      if spl[0] == "NAME":
        name = spl[1].strip()
      if spl[0] == "SEQUENCE":
        seq = spl[1].strip()
      if spl[0] == "STRUCTURE":
        struc = spl[1]
      if "REACTIVITY" in spl[0]:
        reactivities[spl[0]] = spl[1:]
      for r in reactivities:
        counter = 0
        for measurement in reactivities[r]:
          m = float(measurement)
          reactivities[r][counter] = m
          counter += 1

    if normalize_reactivities:
      for r in reactivities:
        nlargest = heapq.nlargest(1, reactivities[r])
        normalizer = sum(nlargest) / len(nlargest)
        counter = 0
        for m in reactivities[r]:
          m /= normalizer
          if m < 0.0:
            m = 0.0
          reactivities[r][counter] = round(m, 5)
          counter += 1

    return {
      "name": name,
      "sequence": seq,
      "structure": struc,
      "reads": 0, # We don't have this info here
      "data": reactivities
    }

  @staticmethod
  def rdats_to_json_file(base_path):
    pass


# Test
path = "../../data/MTTR15_DMS_0001.rdat"

info = RDATPreprocessing.rdat_to_json_record(path, True)
print(info)
# For this particular one, the first set of reactivities is the DMS data


rdat_root = "/common/yesselmanlab/ewhiting/data/rmdb_data/good_rdats"
file_of_rdats = f"{rdat_root}/rdats_with_dms.txt"
