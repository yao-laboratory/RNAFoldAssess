# RNAFoldAssess Tutorial

This tutorial will guide users on how to use RNAFoldAssess. It will cover a brief description of the package's purpose, then run through some examples with data provided in the `./example` directory.

# Purpose

The purpose of the RNAFoldAssess package is to compare the performance of multiple RNA secondary structure prediction tools. The package comes with some predictor models, scoring schemes, and utility functions to support unbiased evaluation. The package is also able to be extended to add other predictor models or scoring schemes and provides instructions for how to do so.

## Overview

Typically, an RNAFoldAssess user will either have a new set of RNA secondary structure data, or a new secondary structure predction model. In either case, the typical goal is to evaluate two or more models against one or more set of data. In either case, the user will pick some number of prediction algorithms to run on some set of data, and then evaluate the performance of each model on each set of data. RNAFoldAssess supports prediction models by wrapping the tool in a `predictor` class. The model's prediciton of a secondary structure is then scored via some scoring scheme. Scoring schemes are supported in RNAFoldAssess via the `Scorer` base class. RNAFoldAssess comes with 3 different scoring schemes, one for chemical mapping, and two for known structure; one that accounts for pseudoknots and one that doesn't.

## Example Use Cases

### Evaluating a new model

Say you have developed a new secondary structure prediction tool and want to compare it with existing tools such as SPOT-RNA and EternaFold. You may decide to run each tool against the PDB RNAs and compare scores. In this case, you would create a wrapper class in the `models/predictors` directory for your tool, as well as one for SPOT-RNA and EternaFold, then create a pipeline for ingesting the data, producing the predictions, scoring the predictions, and comparing the output.

### Evaluating a new sest of RNA data

Another use case for RNAFoldAssess is to evaluate how difficult or easy your new RNA library is to predict. For such a use case, you would likely want to collect performance information on two or more secondary structure prediction models on your new data, as well as some existing data. In this case, you would create a wrapper class for each model and create multiple pipelines to collect performance data on both your new data and existing data.

## Evaluating a new training set of RNA data

As something of a combination of the previous two use cases, perhaps you have developed a new set of RNA data for model training purposes and have used it to retrain an existing model. In this case, you will likely have the out-of-the-box model and the retrained model and want to compare their performance on existing RNA datasets. For such a use case, you will need one wrapper predictor class for the retrained model and one for the default model, then you will create a pipeline to predict and score their performance against another dataset.


# Setting up an Evaluation Pipeline

In this section, we will use the example data in `/tutorial` to set up an example pipeline.

## Step 1 - Loading the Data

in RNAFoldAssess, the `DataPoint` object is the main starting point for almost all operations supported by the package. The `DataPoint` object contains all the data of an individual RNA, such as:
* *Name* - a unique identifier for the RNA
* *Sequence* - the nucleotide sequence of the RNA
* *Ground Truth Data* - This is the RNA's structural data. The ground truth can be either a dot-bracket notation (DBN) string or a collection of chemical reactivities at given nucleotides in the RNA.
* *Cohort (optional)* - This is used for grouping RNAs of similar origin together for future detailed analysis. It is optional and thus does not have to be supplied.

Imagine you have an RNA and chemical reactivity data for it. It might look like this:

```
RNA name: Sequence 001
Cohort: DMS Run 5
Sequence: AAACCCUUUGGG
Reactivities: 0.5, 0.5, 0.1, 0.7, 0.3, 0.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
```

You could create a `DataPoint` object directly from this data by hardcoding it into a Python script:

```python
name = "sequence_001"
cohort = "DMS_Run_5"
sequence = "AAACCCUUUGGG"
reactivities = {
    0: 0.5, 1: 0.5, 2: 0.1,
    3: 0.7, 4: 0.3, 5: 0.7,
    6: 0.0, 7: 0.0, 8: 0.0,
    9: 0.0, 10: 0.0, 11: 0.0
}

dp = DataPoint(
    name=name,
    sequence=sequence,
    ground_truth_type="DMS",
    ground_truth_data=reactivities,
    cohort=cohort
)
```

However, RNAFoldAssess comes with methods to import large quantities of this kind of data into a `list` of `DataPoint` objects. The most accessible way is to prepare a CSV file with the following headers:

```
name,sequence,ground_truth_type,ground_truth_data
```

Fill the CSV rows with the adjacent data and use the `init_from_csv_file` method on `DataPoint` as shown in `tutorial/tutorial_scripts/01_loading_data.py`. Running this method will return a list of `DataPoint` objects.

### How to record `ground_truth_data` in the CSV

`DataPoint` objects have a `ground_truth_data` attribute that contains structural data about the RNA. This data is used in the scoring step of the package when a prediction is evlauted against the known data (i.e., the `ground_truth_data`). This can be a dot-bracket notation (DBN) string, or a reactivity map in the case of reactivities.

If a DBN string is being used for `ground_truth_data`, the `ground_truth_type` value needs to be either "DBN" or "dbn". If the `ground_truth_data` is from chemical probing experiments, the `ground_truth_type` needs to be either "DMS", "SHAPE", or "CMCT".

The ***reactivity map*** is a string that has a nucleotide position followed by a reactivity measure, separated by a semicolon (`;`). So if you have the sequence `AACCUUGG`, and you have DMS reactivities for only the first (0.5), third (0.1), and fourth (0.4) nucleotides, your map would look like this:

```
0:0.5;2:0.1;3:0.4
```

Notice that the nucleotide numbers are 0-indexed, so the first nucleotide is at position 0.

You can see an example of a SHAPE data CSV in `tutorial\processed_data\example_data_chem_mapping.csv`, and an example of structural data (that is, with DBN strings instead of reactivity data) in `tutorial\processed_data\example_data_structure.csv`.
