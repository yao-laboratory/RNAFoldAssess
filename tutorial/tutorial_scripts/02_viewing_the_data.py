from RNAFoldAssess.models import DataPoint
from RNAFoldAssess.models.predictors import RNAFold


"""
In this file, we will use the data we pre-processed in script 01. There should
be a file in tutorial/processed_data example_data.json. We will use this JSON
file to generate a Python list of `DataPoint` objects. We will then instantiate
two predictor models, make them predict a secondary structure for each RNA in
the example data, and save the predictions for comparison and scoring later.
"""

data_path = "../processed_data"
json_file = f"{data_path}/example_data.json"

# First, we'll use the DataPoint `factory_from_json` method to create a list
# of `DataPoint` objects.
datapoints = DataPoint.factory_from_json(json_file)

# Let's briefly explore what a datapoint looks like. The `DataPoint` object
# has a `name` attribute so the individual RNA can be uniquely identified.
# The `DataPoint` object also has, among other attributes, a `sequence`
# attribute--its nucleotide sequence. Let's look at them:
for dp in datapoints:
    print(f"DataPoint {dp.name} -\nSequnece: {dp.sequence}")

# With the example data, the loop above outputs the following:
"""
DataPoint ETERNA_R48_0001 -
Sequnece: GGAAAGCUACGAGGAUAUGCGUAUCACAAAAGUGAUACGGUGGCAUCAAAAGAUGGCACCGAUGAUCAAAAGAUCAUCGCAGAAGGCGUAGCAAAGAAACAACAACAACAAC
DataPoint ETERNA_R49_0001 -
Sequnece: GGAAAGCGUGAAGGAUAUCGCUGCUACGCAAGUAGCAGACUGGCAUGGAAACAUGGCAGUGCGUCACGAAAGUGACGUCGAGAAGGUCACGCAAAGAAACAACAACAACAAC
"""

# Notice also that we have two similar attributes, `reactivities` and
# `reactivity_map`. This is because sometimes, we are given chemical
# probing data for only a portion of a sequence. See the output from
# the following code:

for dp in datapoints:
    seq = dp.sequence
    reactivities = dp.reactivities
    print(f"DataPoint {dp.name} has a sequence of {len(seq)} nucleotides, ")
    print(f"but only has reactivity data for {len(reactivities)} nucleotides")
    print()

# With the example data, the loop above outputs the following:
"""
DataPoint ETERNA_R48_0001 has a sequence of 112 nucleotides,
but only has reactivity data for 80 nucleotides

DataPoint ETERNA_R49_0001 has a sequence of 112 nucleotides,
but only has reactivity data for 80 nucleotides
"""
