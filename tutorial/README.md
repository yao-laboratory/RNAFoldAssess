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
