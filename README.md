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

![image](https://github.com/yao-laboratory/RNAFoldAssess/assets/47164199/fb0c9107-4901-40f3-8cda-186935cf9b9d)

## `models`

### `DataPoint`

### Scorer

In this module, we put different scoring algorithms. For example, the DSCI scorer--which uses the Mann-Whitney U-test--is encapsulated in the `DSCI` class. All classes in this module must inherit the base `Scorer` class and override the `evaluate method`. Note that the `Scorer` class is instantiated with a `DataPoint` object, algorithm name (e.g., EternaFold), and an optional parameter called `evaluate_immediately`. The `evaluate_immediately` parameter defaults to `True` and is used to indicate if the user wants the secondary structure prediction to be scored as soon as the `Scorer` object is instantiated. In other words, when `evaluate_immediately` is `True`, the `evaluate` method will be called at the end of the `__init__` method. If not, the user will have to manually call the `evaluate` method on the `Scorer` object.

### `predictors`

This file contains classes that encapsulate different ways in which the algorithms must be executed and evaluated. For example, the `Eterna` class calls the prediction method for EternaFold on a given sequence file. Conversely, the `SPOT_RNA` class executes the prediction algoirthm, but also converts the output `.ct` files into a secondary structure dot-brakcet string so the predictions can be evaluated.

## `script.py`

This file simply exists to test and show examples of how to use the `executions` models and evaluations.

## TODO

This project has a long way to go. Currently, some of the work remains to standardize inputs and make it painfully obvious how users can add new tools.
