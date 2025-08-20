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

## Step 1 - Data preprocessing

RNAFoldAssess provides a class called `DataPoint`; objects of this class represent single RNAs and should contain at the very least a name, nucleotide sequence, ground-truth data, and an indication of the kind of ground-truth data in the datapoint.

The `DataPoint` class provides methods for instantiating objects from a variety of sources. However, the most reliable and standardized source for the `DataPoint` class is JSON. In the file `tutorial/tutorial_scripts/01_preprocess_data.py`, we convert some raw chemical mapping data into a suitable JSON file that can be ingested by the `DataPoint` class for future use.

In `tutorial/unprocessed_data`, we provide two .rdat files, files that represent chemical mapping readings from the EternaBench project. This kind of data provides a useful example because the rdat files contain RNA sequences and chemical probing reactivities. In the example script, we parse both .rdat files and build a list of dictionary objects from them. The list is then used to write a JSON file that can be used later by the `DataPoint` method, `factory_from_json`.

The example shows how to work with chemical mapping data--specifically, SHAPE data. For chemical mapping data, RNAFoldAssess can also work with DMS and CMCT data. Additionally, RNAFoldAssess can work with a ground-truth data of a given structure. In such cases, the standardized format for a `DataPoint` object is a dot-bracket notation (DBN) string. This package comes with utitlity functions for generating DBN strings from various sources such as .bpseq files and .ct files.

## Step 2 - Viewing the data

To ensure we properly preprocessed the raw data, we will now use the `DataPoint` method `factory_from_json` to create a Python `list` of `DataPoint` objects. We will also look at some of the attributes the `DataPoitn` class provides. Take a look at the script in `tutorial/tutorial_scripts/02_viewing_the_data.py` for a more hands-on look at this class.

The `DataPoint` object has many attributes and methods in an attempt to concisely and intuitively encapsulate all the data an individual RNA may have.

`name` - this attribute is used to uniquely identify an RNA for downstream analysis. While many RNAs can be identified by their sequence, the combination of a sequence and ground truth data may be unique. In either case, the `name` of a `DataPoint` is a conventient way to uniquely identify an RNA.

`cohort` - this attribute is similar to `name` but is used to identify a batch or collection of common RNAs. For example, you may have run 3 DMS experiments, each with sequence_1, sequence_2, and sequence_3. Perhaps you named the experiments run1, run2, and run3. In such a case, you would use the `cohort` to separate each sequence based on its run. You would have a set of `DataPoint` objects whose cohort is run1, a set where the cohort is run2, and a set where the cohort is run3. Altogether, the RNAs in your collection of data would have the following names:

```
run1_sequence_1
run1_sequence_2
run1_sequence_3
run2_sequence_1
run2_sequence_2
run2_sequence_3
run3_sequence_1
run3_sequence_2
run3_sequence_3
```

`sequence` - this attribute represents the nucleotide sequence of the RNA. It does not natively make any changes to the sequence such as capitalizing letters or changing T to U. In other words, there is no error-correcting around the `sequence` attribute, so any translation that must be done to a sequence should be done in the data preprocessing step. This is because some secondary structure prediction algorithms can handle other letters of the RNA alphabet such as N or X for "any base" or R for purine. It is up to the researcher to decide how the sequences should be preprocessed.


