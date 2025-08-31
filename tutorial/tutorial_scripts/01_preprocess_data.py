from RNAFoldAssess.models import DataPoint


"""
RNAFoldAssess can generate DataPoint objects from JSON files as long as
each datapoint in the JSON file has at least the following keys:

  name
  sequence

The JSON object also needs a ground-truth type; either a DBN string or
some kind of chemical mapping readings. Since the example data is from
a chemical mapping experiment, the JSON should have a key called
position_map that aligns a reactivity reading to a position in the RNA
sequence, and experiment_type that indicates what kind of chemical mapping
was used int he experiment. In the following script, we will build this object.
"""

raw_data_path = "../unprocessed_data"

datapoints = DataPoint.init_from_rdat_files(raw_data_path)
breakpoint()
print(":)")
