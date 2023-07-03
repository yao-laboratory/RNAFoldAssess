# Analyzing RNA secondary structure prediction algorithms

This repository evaluates different secondary structure prediction algorithms. The basic workflow is:
* The input is a sequence of RNA nucelotides (and in some cases, other inputs as well)
* We pass that input into a model (i.e., RNAfold, EternaFold, SPOT-RNA, etc.)
* The model outputs a secondary structure prediction based on the input
  * This output could come in several forms, but we want the dot-bracket notation
  * If the output is in anything besides a dot-bracket string, convert it to db somehow (like in the case of SPOT-RNA)
* Evaluate the prediction's accuracy
  * So far, we do this by comparing experimentally-derived reactivities of RNA structures with the output of the dot-bracket notation
  * There are other ways to evaluate accuracy but with the `ss_deeplearning_data` repository, this is the best evaluation so far

Once more prediction algoirthms are identified and support for their functionality are added, I intend to build a database of evaluations. The databse will contain
* Evaluation of each algorithm and for each datapoint
* A ranking of the "best" and "worst" algorithms
* A list of common structures that are incorrectly guessed

# Code organization

This explains the different code files and will grow as time goes

## `/models`

This module contains different models to accomplish the various tasks.

### `DataPoint`

This is all the data for a single RNA structure. It records the name, sequence, and reactivities of the structure. In the future, it may contain other informaiton that help evaluate the performance of each algoritm.

### `executions.py`

This file contains classes that encapsulate different ways in which the algorithms must be executed and evaluated. For example, the `Eterna` class calls the prediction method for EternaFold on a given sequence file. Conversely, the `SPOT_RNA` class executes the prediction algoirthm, but also converts the output `.ct` files into a secondary structure dot-brakcet string so the predictions can be evaluated.

### `Prediction`

This class contains all the data necessary to analyze a prediction's performance. As of right now it contains an `accuracy` and `p_value` attribute, and a  `metrics` attribute that describes everything one might need to know for future evaluation.

## `test_script.py`

This file simply exists to test and show examples of how to use the `executions` models and evaluations.

