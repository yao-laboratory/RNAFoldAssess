# RNAFoldAssess
A framework for comparing RNA secondary structure prediction algorithms

# Installation

RNAFoldAssess is not yet available on the Python Package Index. In the meantime, you can either download the package by clicking the "Code" button in the top right corner of this GitHub page and selecting "Download ZIP" and then extracting the compressed file.

You can also download the repository via Git with the following command:

```bash
git clone git@github.com:yao-laboratory/RNAFoldAssess.git
```

Once you've either extracted the compressed folder or downloaded the repository from git, you install the framework with the following commands:

```bash
cd RNAFoldAssess
python -m venv rfa_env # Create the virtual environment
source rfa_env/bin/activate # Activate the virtual environment
pip install -r requirements.txt # Install package's requirements
pip install -e . # Install this package
```

NOTE: You may have to use `python3` or `py` or another command instead of `python` from the example above. Use the same command you use to open a python terminal.

Now, let's make sure the installation was successful. Either run the following code a script or line by line in the Python terminal:

```python
from RNAFoldAssess.models import BasePairScorer

# Simulated "real" and "predicted" secondary
# structures in dot-bracket notation
real_structure =      ".(..)..(.(..))."
predicted_structure = ".(...)...(..).."

scorer = BasePairScorer(real_structure, predicted_structure)
scorer.evaluate()
report = scorer.report(precision=5)

print(report) # Sensitivity: 0.33333, PPV: 0.5, F1: 0.4
```

If the value of `report` is `Sensitivity: 0.33333, PPV: 0.5, F1: 0.4` then everything installed successfully!

# Usage

RNAFoldAssess is a framework for comparing the effectiveness of RNA secondary structure prediction tools. Let's consider an example.

## A Simple Example

You collected SHAPE readings on an RNA with the sequence ACUGACUGAAAAAAAA and got the following readings:
```
0.750, 0.875, 0.493, 0.280, 0.662, 0.478, 0.223, 0.360, 0.840, 0.883, 0.608, 0.988, 0.933, 0.685, 0.673, 0.673
```

And you have three secondary structure prediction tools that you want to evaluate: RNAFold, MXFold2, and ContraFold. Assuming you have a `Predictor` class for each tool, we create an object of each class, then run each object's `execute` method:

```python
from RNAFoldAssess.models import *

sequence = "ACUGACUGAAAAAAAA"

rna_fold = RNAFold()
mxfold2 = MXFold2()
contra_fold = ContraFold()

rna_fold.execute(sequence)
mxfold2.execute(sequence, "path/to/mxfold2")
contra_fold.execute(sequence, "path/to/contrafold")
```

The `execute` method sets each object's `output` attribute, from which we extract the secondary structure predition with the method `get_ss_prediction`:

```python
rf_pred = rna_fold.get_ss_prediction()
mx_pred = mxfold2.get_ss_prediction()
cf_pred = contra_fold.get_ss_prediction()
```

Let's see what the different tools predicted

```python
print(rf_pred) # ................
print(mx_pred) # ..(......)......
print(cf_pred) # ..(.......).....
```

We have three distinct predictions, now to evaluate which prediction tool had the best prediction, we see which predicted structure most agrees with the SHAPE data. To do this, we use the DSCI scorer.

```python
from RNAFoldAssess.models.scorers import DSCI

reactivities = [0.750, 0.875, 0.493, 0.280, 0.662, 0.478, 0.223, 0.360, 0.840, 0.883, 0.608, 0.988, 0.933, 0.685, 0.673, 0.673]

rf_score = DSCI.score(sequence, rf_pred, reactivities, SHAPE=True)
mx_score = DSCI.score(sequence, mx_pred, reactivities, SHAPE=True)
cf_score = DSCI.score(sequence, cf_pred, reactivities, SHAPE=True)
```
The `DSCI.score` method returns a Python dictionary with the keys `accuracy` and `p`. The value with `accuracy` is the AROC from Mann-Whitney U-test, and the value with `p` is the p-value from the test. The higher the `accuracy` value, the more the predicted structure agrees with the SHAPE reactivities. Therefore, whichever score variable has the highest `accuracy` value is the most-correct prediction.

## Scorers

The RNAFoldAssess package comes with three scorers, `DSCI`, `BasePairScorer`, and `BasePairPseudoknotScorer`. The `DSCI` scorer is used for RNA predictions where the ground-truth of the structure is chemical mapping data, the other two scorers are used for RNA predictions where the ground-truth of the structure is a dot-bracket notation (dbn) string.

### DSCI

The `DSCI` scorer implements the Mann-Whitney U-test and evaluates a sequence and a dbn-formatted prediction against chemical mapping data (the ground-truth for that RNA). The score is returned as a two-item dictionary with `accuracy` and `p` keys, the `accuracy` being the calculation of the U-test, and the `p` being the p-value of the test.

The `DSCI.score` method wokrs for SHAPE and DMS reactivities. In the case of DMS, reactivities aligned with guanine (G) and adenine (A) are not factored into the calculation, as DMS does not react with those nucleotides.

Users can extract a DSCI score by either instantiating a `DSCI` object with a `DataPoint` object (discussed later) and call the `evaluate` method, or with the static `score` methd, which takes a sequence, dbn prediction, reactivities list, and experiment-indication parameters (either `DMS=True` or `SHAPE=True`).

### BasePairScorer

The `BasePairScorer` class calculates the sensitivity, postiive predicted value (PPv) and F1 score of a predicted secondary structure. To extract the scores, users have to instantiate a `BasePairScorer` class with the true structure and predicted structure as dbn strings. Users can optionally provide a lenience allowance (discussed later).

An example implementation:

```python
from RNAFoldAssess.models.scorers import BasePairScorer

real_structure = ".(..)..(.(..))."
predicted_structure = ".(...).(.(..))."
scorer = BasePairScorer(real_structure, predicted_structure)
scorer.evaluate()
print(scorer.report()) # Sensitivity: 0.667, PPV: 0.667, F1: 0.667
```

Optionally, users can allow n-basepair lenience for the scoring function. To explain what this means, consider the two secondary structures from the previous example:

```
real_structure =      ".(..)..(.(..))."
predicted_structure = ".(...).(.(..))."
```

The structures are nearly identical, but the closing parethese for the first base pair is predicted to be one nucleotide closer to the 3' end than the actual structure. This means that the predicted structure is 1 basepair away from being a perfect prediction. You can configure the scorer to allow for n-basepairs of inaccuracy by instantiating the `BasePairScorer` object with a `lenience` parameter. In this case, we will set the `lenience` to 1:

```python
from RNAFoldAssess.models.scorers import BasePairScorer

real_structure = ".(..)..(.(..))."
predicted_structure = ".(...).(.(..))."
scorer = BasePairScorer(real_structure, predicted_structure, 1)
scorer.evaluate()
print(scorer.report()) # Sensitivity: 1.0, PPV: 1.0, F1: 1.0
```

The only difference between this code and the example above it is passing the value of `1` to the constructor. When we do so, the calculated sensitivity, PPV, and F1 score are all 1.0, indicating a perfect prediction.

The `BasePairScorer` calculates its score metrics by parsing the ground-truth structure and extract a list of two-tuples representing the string coordinates of paired nucleotides. For example, the string coordinates of paired nucleotides for the dbn string `.(..)..(.(..)).` is `[(1, 4), (7, 13), (9, 12)]`. The scorer object then parses the predicted structure and extracts a list of two-tuple string coordinates for the predicted base pairs. Then, the scorer loops through the predicted coordinates and checks if they are present in the true coordinates. If a predicted coordinate is present in the list of true coordinates, that is considered a *true positive (tp)*. If a predicted coordinate is not in the list of true coordinates, that is considered a *false positivie (fp)*. Finally, the scorer loops through the coordinates of the true structure. If a coordinate in the true structure list is not present in the predicted structure coorinates, that is considered a *false negative (fn)*.

When a lenience parameter is given, the scorer calculates a list of "acceptable coordinates" based on the true structure. For example, given a `lenience` of 1 basepair for the example structure above, the acceptable coordinates are

```python
[
  (1, 3), # Actual coordinate
  (0, 3), (1, 2), (2, 3), (1, 4),

  (6, 14), # Actual coordinate
  (5, 14), (6, 13), (7, 14), (6, 15),

  (9, 11), # Actual coordinate
  (8, 11), (9, 10), (10, 11), (9, 12)
]
```
The predicted structure is then evaluated in the same way, but instead of checking its coordinates against those of the true structure, it is checked against the acceptable coordinates list.

Note, the scorer ignores all characters that are not either a period (`.`) or parentehses (`(` or `)`). Pseudoknot symbols and other wildcard symbols (such as `{`, `[`, `X`, and so on) are ignored.

### BasePairPseudoknotScorer

Some secondary structure prediction tools are capable of predicting pseudoknots. To score the accuracy of such tools, RNAFoldAssess provides the `BasePairPseudoknotScorer` class. This class behaves idenitcally to the `BasePairScorer` class, except that it also gathers coordinate information for pseudoknots that are desginated in the dbn string with square brackets (`[` and `]`)

### Adding a Custom Scorer

Some researchers may want to customize the scoring method while still using the RNAFoldAssess framework. To do so, add a `.py` file to the `models/scorers` directory and create a class that inherits `Scorer`. The `Scorer` class is a base class that defines the two methods a scorer class needs to plug into the framework: `evaluate` and `report`. The `scorer.py` class has more detailed instructions for implementing a new scorer. Scoring methods should base their calculations on a prediction in dbn format, as these are what the `Predictor` models output.

## Predictors

The classes present in the `models/predictors` directory are wrapper classes for the RNA secondary structure prediction tools to be evaluated. Each class inherits the base `Predictor` model which declares `execute` and `get_ss_prediction` methods. Any tool that will be evaluated within the RNAFoldAssess framework must be accessed through a `Predictor` class. This is because during the evaluation portion of a benchmarking pipeline, the framework will call `execute` and `get_ss_prediction` to extract the tool's secodary structure prediction and (if necessary) transform it into a dbn string for scoring. More detailed tips for creating new `Predictor` classes can be found in the docstrings in `models/predictors/predictor.py`.

Some prediction tools have Python wrappers that can be used in the same way third-party libraries are used (The ViennaRNA RNAFold tool is an example). In these cases, the `Predictor` model will simply utilize the tool package's API to create the `execute` and `get_ss_prediction` methods.

More often, prediction tools are only provided as command line tools or copmiled binaries. In these cases, the `execute` method will have to invoke the tool by interfacing with the command line and read the output somehow. This can be accomplished by either using the Python `os` library's `system` method and writing the output to a temporary file so the class's `output` attribute can save the tools output for further processing, for example:

```python
import os

class SomeNewPredictor(Predictor):
  ...
  def execute(self, rna_sequence, path_to_tool):
    exec_string = f"{path_to_tool} {rna_sequence} > prediction_from_{self.name}.txt"
    os.system(exec_string)
    with open(f"prediction_from_{self.name}.txt") as fh:
      self.output = fh.read()

    os.remove(f"prediction_from_{self.name}.txt")
```

Another method, though one that can sometimes be slightly less reliable, is to use the `popen` method from `os`. A similar implementation with this approach might look like this:

```python
import os

class SomeNewPredictor(Predictor):
  ...
  def execute(self, rna_sequence, path_to_tool):
    exec_string = f"{path_to_tool} {rna_sequence}"
    self.output = os.popen(exec_string).read()
```

Once the tool is executed and its output is stored in the class's `output` attribute, implement `get_ss_prediction` to parse the output and extract a dbn string represntation of the prediction. Many tools output a dbn string already and all you have to do is parse the rest of the output. Other tools may generate files like a `.ct` or `.bpseq` file, which would have to parsed to created a dbn string. In either case, the `get_ss_prediction` method should return a dbn string with no whitespace characters.

The RNAFoldAssess package comes with two `Predictor` models to help users get started in writing their own (or using existing tools), the `RNAFold` model an the `RNAStructure` model.

The `RNAFold` model is a wrapper class for the RNAfold program from ViennaRNA. The maintainers of that package provide Python bindings for the tool which are available on PyPI. As such, this model is ready for use as soon as users install the requirements in `requirements.txt`. The `execute` and `get_ss_prediction` methods are already implemented and ready for use.

Conversely, the `RNAStructure` class wraps the `Fold` program from the RNAStructure suite of tools. This tool does not have Python bindings available on PyPI and thus must be used as a command line tool. The `RNAStructure` class uses the `os.popen` method to extract this tool's output. Please note that this tool **assumes the user already has RNAStructure installed on their machine**. If you do not have the Fold program in your PATH and the tool's environmental variables set, this class will not work after installation. If you do have the tool already configured though, this class should work as seamlessly as the `RNAFold` class.

The `RNAStructure` class is provided as an example to users who wish to evaluate command-line tools. It is important to note that such tools must be installed and configured before a `Predictor` class wrapping them is usable.

## DataPoint

The `DataPoint` class is meant to encapsulate different representations of RNAs and provide several convenience features to users.

### Attributes

**`name`**: What an RNA is referred to. For example, 5NXT_chain_A might be the name of a datapoint.

**`sequence`**: The nucleotide sequence of an RNA.

**`ground_truth_type`**: The concept of "ground truth" is what this framework uses to evaluate the efficacy of secondary structure predictions. Currently, the framework supports two kinds of ground truth data: dot-bracket notation string, and chemical mapping reactivities (either DMS, SHAPE, or CMCT). The acceptable values for this attribute are "DMS", "SHAPE", "CMCT", or "dbn".

**`ground_truth_data`**: This attribute is the representation of the ground truth data for an RNA's secondary structure. If the `ground_truth_type` is `"dbn"`, then the `ground_truth_data` value should be a string in dot-bracket notation. If the `ground_truth_type` is one of the chemical mapping values, the `ground_truth_data` attribute is a list of reactivities from a chemical mapping experiment; the order of reactivites must line up with the order of nucleotides. That is, reactivities must be ordered from 5' to 3'.

**`cohort`**: This attribute is for organization purposes and is used as a prefix to the `DataPoint` object's name. For example, if you have three sets of data called "DMS1", "DMS2", and "DMS3", you may want to differentiate those in your analysis. In such case, you would set the `cohort` attribute to the name of the data set. For example, if you have an RNA in DMS2 called "hairpin_structure_11", its `name` attribute would be `DMS2_hairpin_structure_11`.

**`reads`**: Chemical mapping data sometimes includes a number of reads, if the user wants to capture that data, this attribute supports it.

**`reactivities`**: If the `ground_truth_type` is of a chemical mapping type, the `reactivities` attribute will return the same thing the `ground_truth_data` returns; i.e., a list of reactivities. If not, trying to access this attribute will raise an exception.

**`structure`**: If the `ground_truth_type` is "dbn", the `structure` attribute will return the same thing as the `ground_truth_data`, which should be a dot-brack notation string. e.g., `...(((...)))...`. If not, trying to access this attribute will raise an exception.

### Initialization methods

A `DataPoint` object can be initialized in many ways, the only required attributes at initialization are a name and nucleotide sequence. You can initialize it with the default constructor method such as:

```python
dp = DataPoint(
  "hairpin_11",
  "AAAACCCCAAAAGGGGUUUU",
  ground_truth_type="dbn",
  ground_truth_data="....((((....))))....",
  cohort="lab_data"
)
```

There are also several initialization methods:

**`init_from_dict`**: This method takes a dictionary object and optional `name` or `cohort` as parameters. The dictionary will look for the keys `name`, `sequence`, `reads`, `data`, and `dbn`. If those are not found, they are set to `None`. If a `name` parameter is provided to the method, it will overwrite the `name` value in the dictionary. If there is no `name` parameter provided and no `name` key in the dictionary, this method assume the dictionary is of type `{ "some_name": {"sequence": "*some sequence*", ..., }}` and use the first key of the object as the datapoint's name and extract the values from that key. Here's an example of initializing a datapoint from this method:

```python
data = {
  "hairpin_11": {
    "sequence": "AAAACCCCAAAAGGGGUUUU",
    "dbn": "....((((....))))....",
    }
}
```

TODO:

**`init_from_fasta`**:

**`init_from_dbn_file`**:

**`init_from_seq_file`**:

**`factory_from_json`**


## Example Pipeline

TODO

# Contact

For any questions, please contact Erik Whiting at `ewhiting4@unl.edu`
