from RNAFoldAssess.models import DataPoint


"""
The DataPoint object is the main starting point for all of the RNAFoldAssess
functionality. The most accessible form of raw data is the CSV file. In our
examples, we'll use the example files found in tutorial/processed_data.
Specifically, we'll use
    - example_data_chem_mapping.csv
    - example_data_structure.csv

The former is a CSV file that will build DataPoint objects whose ground truth
structure data is recorded via chemical mapping, the latter is a CSV file
that will build DataPoint objects whose ground truth structure data is
recorded via dot-bracket notation.
"""

raw_data_path = "../processed_data"

# Let's import the structure CSV
datapoints = DataPoint.init_from_csv_file(f"{raw_data_path}/example_data_structure.csv")

# Let's view some of that data to see how the DataPoint object works:
print()
for dp in datapoints:
    print(f"DataPoint name: {dp.name}")
    print(f"Sequence:  {dp.sequence}")
    print(f"Structure: {dp.structure}")
    print()

