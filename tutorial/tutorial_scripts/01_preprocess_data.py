import json, os


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
files = os.listdir(raw_data_path)

datapoints = [] # This will be turned into our processed JSON file
for f in files:
    with open(f"{raw_data_path}/{f}") as fh:
        rdat_data = fh.readlines()

    # Find the first "ANNOTATION_DATA" entry

    annotation_data_line = ""
    for line in rdat_data:
        if line.startswith("ANNOTATION_DATA"):
            annotation_data_line = line
            break

    # The line is delimted by tabs
    annotation_data = annotation_data_line.split("\t")

    # The chemical type is in an item that starts with "modifier"
    # It's written as "modifier:type"
    for ad in annotation_data:
        if "modifier" in ad:
            experiment_type = ad.split(":")[1]
            break

    print(f"Experiment type: {experiment_type}") # SHAPE

    # The sequence is in an item that starts with "sequence"
    # It's written as "sequence:XXXX..XX"

    for ad in annotation_data:
        if "sequence" in ad:
            sequence = ad.split(":")[1].strip() # Remove \n character
            break

    print(f"Sequence: {sequence}") # GGAAAGCGUGAAG...CAAC

    # The positions for which the readings are available are annotated
    # in a line that starts with SEQPOS

    seqpos_line = ""
    for line in rdat_data:
        if line.startswith("SEQPOS"):
            seqpos_line = line
            break

    # SEQPOS annotates the positions in a 1-indexed list like this:
    # X1, X2, X3
    # We will split the line, remove the X's, and subtract 1 from the number
    positions = []
    for pos in seqpos_line.split("\t")[1:]: # Ignore the first item that is "SEQPOS"
        pos = pos.replace("X", "") # remove the X
        pos = int(pos) - 1
        positions.append(pos)

    print(f"Positions with chemical probing data: {positions}")

    # Now we get the first line of reactivities. Since we used ANNOTATION_DATA:1,
    # we will use the REACTIVITY:1 line.

    reactivity_line = ""
    for line in rdat_data:
        if line.startswith("REACTIVITY:1"):
            reactivity_line = line
            break

    # Reactivities are separated by tabs, we just need to make them into floats
    reactivities = []
    for r in reactivity_line.split("\t")[1:]:
        reactivities.append(float(r))

    print(f"Reactivities: {reactivities}")

    # Finally, we just need to extract a name. In general, the name needs to be something
    # you can use to cross-reference the datapoint later. In this case, the file name
    # should be good enough for this datapoint
    name = f.replace(".rdat", "")
    print(f"Name: {name}")

    # Now we just build the datapoint along with its reactivity map
    datapoint = {
        "name": name,
        "sequence": sequence,
    }

    reactivity_map = {}
    for i, p in enumerate(positions):
        reactivity_map[p] = reactivities[i]

    datapoint["reactivity_map"] = reactivity_map

    # Now just append the datapoint to the `datapoints` variable
    datapoints.append(datapoint)

# Now we write the data to JSON
with open("../processed_data/example_data.json", "w") as fh:
    json.dump(datapoints, fh)
