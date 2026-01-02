![RNAFoldAssess Logo](RNAFoldAssess_logo_v1.png)

# RNAFoldAssess
A framework for comparing RNA secondary structure prediction algorithms

# 1 Purpose and Overview

The purpose of the RNAFoldAssess package is to compare the performance of multiple RNA secondary structure prediction tools. A secondary structure prediction tool typically takes an RNA sequence as input, and outputs a prediction of what basepairs that RNA sequence will form; this is called the secondary structure. When ground truth for that RNA is available (e.g., known structures or chemical-probing reactivities), predictions can be evaluated against it and assigned numerical scores.

The RNAFoldAssess package offers a framework for building secondary structure prediction tool evaluation pipelines. That is, the components of this package support the evaluation of multiple prediction tools against large quantities of data. The package comes with one wrapped secondary structure prediction tool (RNAFold) ready to use out of the box, and advanced installation instructions for other tools. Additionally, the framework is extendable and has directions on adding your own secondary structure prediction tool to the package. Fianlly, the framework contains scorers for the two main types of RNA ground-truth data (chemical probing readings and dont-bracket notation strings) and instructions for adding your own.

# 2 Quickstart Tutorial

If you want to quickly get up and running to see what RNAFoldAssess can do, check out the [tutorial page](tutorial/README.md). The tutorial page contains installation instructions in addition to this README.

# 3 Installation

RNAFoldAssess is not yet available on PyPI. In the meantime, follow the installation steps outlined below:

## 3.1 Get the files

First, you need the source code. One way you can get it is by clicking the "Code" button in the top right corner of this GitHub page and selecting "Download ZIP" and then extracting the compressed file.

Alternatively, you can download the repository via Git with the following command:

```bash
git clone git@github.com:yao-laboratory/RNAFoldAssess.git
```

## 3.2 Install dependencies and package

Once you've either extracted the compressed folder or downloaded the repository from git, you install the framework with the following commands:

```bash
cd RNAFoldAssess
python -m venv rfa_env # Create the virtual environment
source rfa_env/bin/activate # Activate the virtual environment
pip install -r requirements.txt # Install package's requirements
pip install -e . # Install this package
```

**NOTE**: You may have to use `python3` or `py` or another command instead of `python` from the example above. Use the same command you use to open a python terminal.

# 4 Pipeline Modes

RNAFoldAssess supports the creation of evaluation pipelines with just a few lines of code. Pipelines can run in one of three different modes, summarized in this section.

## 4.1 Mode 1 - Prediction + Evaluation

A pipeline in Mode 1 takes a prediction tool and generates a prediction and evaluation for each RNA in a given dataset. The RNA data needs to include sequence and ground-truth data for this mode to work. The pipeline will take the sequence from each RNA in the data, pass it to the secondary structure prediction tool, extract the prediction, and evaluate that prediction from the given ground-truth data of the RNA. Therefore, for Mode 1 to work, the RNA data has to include ground-truth data (chemical probing reactivities or a dot-bracket notation string of the known structure). Upon completion, the pipeline will write the results to a CSV file.

## 4.2 Mode 2 - Prediction only

A pipeline in Mode 2 takes a prediction tool and generates a prediction for each RNA in a given dataset. This is useful if you have RNA sequence data but don't yet have ground-truth data, or you just want to generate predictions for a large set of data. The pipeline takes the sequence from each RNA in the dataset, passes it to the secondary structure prediction tool, and extracts the prediction. The results are written to a CSV file.

## 4.3 Mode 3 - Evaluation from existing predictions

A pipeline in Mode 3 takes an RNA dataset with ground-truth data and generates evaluations from the predictions generated in Mode 2. This pipeline requires the CSV output from Mode 2 as input as well as RNA data with ground-truth data. It extracts the prediction from the Mode 2 CSV and evaluates it against the ground-truth data and calculates a score. The ***outputs*** from Mode 1 and Mode 3 are the same.


# 5 Advanced Information

## 5.1 Installing Other Secondary Structure Prediction Tools

RNAFoldAssess comes with support for several secondary structure prediction tools, but each individual user needs to install the tools and then update the relevant `Predcitor` class in the package. Please note that while RNAFoldAssess can work on any operating system, some operating systems are not supported by all prediction tools.

***NOTE:*** RNAFold is already supported by this package.

### 5.1.1 ContextFold

Follow the [ContextFold download instructions](https://mybiosoftware.com/context-fold-1-0-rna-secondary-structure-prediction-tool.html) to install the tool. You also need to make sure `java` is in your path. From there, you can use the `ContextFold` class to wrap the tool and use it within this framework.

***NOTE:*** As of November 9th, 2025, it seems the download link to ContextFold is no longer available.


### 5.1.2 ContraFold

To use ContraFold, we used the EternaFold package, but with the ContraFold parameters. To do this, follow the [EternaFold installation instructions](https://github.com/eternagame/EternaFold) and then use the `ContraFold` class.

### 5.1.3 EternaFold

To use EternaFold, simply follow the [EternaFold installation instructions](https://github.com/eternagame/EternaFold) and then use the `Eterna` class. Please note that EternaFold uses the ContraFold program with its own specific parameters, so the execution string has `contrafold` in it.

### 5.1.4 IPKnot

To use IPKnot, follow the [IPKnot installation instructions](https://github.com/satoken/ipknot) and use the `IPKnot` class. Note that IPKnot has an optional `remove_file_when_done` parameter that defaults to `False`. If you set this to true, the fasta file will be deleted after the prediction is made.

### 5.1.5 MXFold

For MXFold, follow the [MXFold installation instructions](https://github.com/mxfold/mxfold) and use the `MXFold` class.

### 5.1.6 MXFold2

To use MXFold2, you need pytorch and possibly a GPU. Follow the [installation instructions for MXFold2](https://github.com/mxfold/mxfold2) and use the `MXFold2` class.

### 5.1.7 NUPACK

To install NUPACK, please visit the [NUPACK downloads page](https://www.nupack.org/download/overview) and follow the installation instructions. For our research, we built the project from source and then included it into the project as a Python module. As such, the `NUPACK` class doesn't need a path to an executable like the other prediction algorithms.

### 5.1.8 RNAStructure

To use RNAStructure, follow [the installation guide](https://rna.urmc.rochester.edu/RNAstructure.html) installation instructions and use the `RNAStructure` class. Note that the RNAStructure tool creates a `.ct` file that RNAFoldAssess then uses to extract a dot-bracket notation string. As such, users need to also pass an `output_path_base` to the `execute` method.

### 5.1.9 pKnots

To install pKnots, see [the INSTALL script on the project's GitHub](https://github.com/EddyRivasLab/PKNOTS/blob/master/INSTALL). You can then use the `pKnots` class. Note that, like RNAStructure, the pKnots tool outputs a `.ct` file. Therefore, the user needs to supply a `ct_dir` to indicate where the `.ct` files should go. There is also an optional `output_subfolder` parameter in the `execute` method to indicate a subfolder for the `.ct` files to go.

## 5.2 Framework Components

### 5.2.1 Scorers

The RNAFoldAssess package comes with two scorers, `DSCI` and `BasePairScorer` (There is an experimental `BasePairPseudoknotScorer` for structures with pseudoknots but it has not yet been thoroughly tested). The `DSCI` scorer is used for RNA predictions where the ground-truth of the structure is chemical mapping data, the other scorer is used for RNA predictions where the ground-truth of the structure is a dot-bracket notation (dbn) string.

#### 5.2.1.1 DSCI

*To learn more abotu this scoring scheme, please refer to the paper [Insights into the secondary structural ensembles of the full SARS-CoV-2 RNA genome in infected cells](https://www.biorxiv.org/content/10.1101/2020.06.29.178343v2.full).*

The `DSCI` scorer implements the Mann-Whitney U-test and evaluates a sequence and a dbn-formatted prediction against chemical mapping data (the ground-truth for that RNA). The score is returned as a two-item dictionary with `accuracy` and `p` keys, the `accuracy` being the calculation of the U-test, and the `p` being the p-value of the test.

The scoring method essentially quantifies the probability that a randomly chosen base predicted to be unpaired will have higher reactivitiy than a randomly chosen unpaired base.

The `DSCI.score` method wokrs for SHAPE and DMS reactivities. In the case of DMS, reactivities aligned with guanine (G) and adenine (A) are not factored into the calculation, as DMS does not react with those nucleotides.

Users can extract a DSCI score by either instantiating a `DSCI` object with a `DataPoint` object (discussed later) and call the `evaluate` method, or with the static `score` methd, which takes a sequence, dbn prediction, reactivities list, and experiment-indication parameters (either `DMS=True` or `SHAPE=True`).

#### 5.2.1.2 BasePairScorer

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

#### 5.2.1.3 BasePairPseudoknotScorer

Some secondary structure prediction tools are capable of predicting pseudoknots. To score the accuracy of such tools, RNAFoldAssess provides the `BasePairPseudoknotScorer` class. This class behaves idenitcally to the `BasePairScorer` class, except that it also gathers coordinate information for pseudoknots that are desginated in the dbn string with square brackets (`[` and `]`)


### 5.2.2 Predictors

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

### 5.2.3 DataPoint

The `DataPoint` class is meant to encapsulate different representations of RNAs and provide several convenience features to users.

#### 5.2.3.1 Attributes

**`name`**: What an RNA is referred to. For example, 5NXT_chain_A might be the name of a datapoint.

**`sequence`**: The nucleotide sequence of an RNA.

**`ground_truth_type`**: The concept of "ground truth" is what this framework uses to evaluate the efficacy of secondary structure predictions. Currently, the framework supports two kinds of ground truth data: dot-bracket notation string, and chemical mapping reactivities (either DMS, SHAPE, or CMCT). The acceptable values for this attribute are "DMS", "SHAPE", "CMCT", or "dbn".

**`ground_truth_data`**: This attribute is the representation of the ground truth data for an RNA's secondary structure. If the `ground_truth_type` is `"dbn"`, then the `ground_truth_data` value should be a string in dot-bracket notation. If the `ground_truth_type` is one of the chemical mapping values, the `ground_truth_data` attribute is a list of reactivities from a chemical mapping experiment; the order of reactivites must line up with the order of nucleotides. That is, reactivities must be ordered from 5' to 3'.

**`cohort`**: This attribute is for organization purposes and is used as a prefix to the `DataPoint` object's name. For example, if you have three sets of data called "DMS1", "DMS2", and "DMS3", you may want to differentiate those in your analysis. In such case, you would set the `cohort` attribute to the name of the data set. For example, if you have an RNA in DMS2 called "hairpin_structure_11", its `name` attribute would be `DMS2_hairpin_structure_11`.

**`reads`**: Chemical mapping data sometimes includes a number of reads, if the user wants to capture that data, this attribute supports it.

**`reactivities`**: If the `ground_truth_type` is of a chemical mapping type, the `reactivities` attribute will return the same thing the `ground_truth_data` returns; i.e., a list of reactivities. If not, trying to access this attribute will raise an exception.

**`structure`**: If the `ground_truth_type` is "dbn", the `structure` attribute will return the same thing as the `ground_truth_data`, which should be a dot-brack notation string. e.g., `...(((...)))...`. If not, trying to access this attribute will raise an exception.

#### 5.2.3.2 Initialization methods

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


# 6 Utility Functions

The RNAFoldAssess package comes with several utility functions for working with chemical mapping data and secondary structure data. While these functions are not part of the core benchmark pipeline building tools, they may be useful to researchers for enriched analysis.

## 6.1 DSSR

The `DSSR` class found in `utils/dssr.py` provides a method called `get_ss_from_pdb` that wraps the [x3DNA DSSR](https://x3dna.org/) tool. The tool assumes you have an environment variable called `DSSR_PATH` that points to the x3na-dssr binary.

**Inputs**

`path_to_pdb` (required) - The path to a `.pdb` or `.cif` file.
`destination_dir` (optional) - Where to you want the output files written to. The default value is the current working directory.

**Outputs**

The file contents of the `.dbn` file output by the DSSR tool. The return value is a `str` data type.

**Side Effects**

Auxiliary files output by the DSSR tool will be written to the `destination_dir` path. All files will be prefixed with the PDB ID of the file in `path_to_pdb`. For example, running the tool agains `1ehz.pdb` will output `1ehz-2ndstr.dbn` to the destination directory.

**Example Usage**

```python
from RNAFoldAssess.utils.dssr import DSSR

dbn_str = DSSR.get_ss_from_pdb('pdb_files/1msy.pdb', 'dssr_file_outputs')
print(dbn_str)
# Will output:
# >1msy nts =27 [ whole ]
# UGCUCCUAGUACGUAAGGACCGGAGUG
# .(((((.....(....)....))))).
# >1msy -A #1 nts =27 0.30(2.47) [ chain ] RNA
# UGCUCCUAGUACGUAAGGACCGGAGUG
# .(((((.....(....)....))))).
```

## 6.2 Normalizers

The methods in the `Normalizers` class are meant to help with normalizing chemical mapping reactivity data.

### 6.2.1 simple_normalizer

Given a list of numeric items, returns a list of floats in which all numbers in the given data are divided by the highest number in the given data. This ensures a list of floats in which all items are between 0 and 1.

**Inputs**

A list of items that can respond to Python's `float` function. For example, all the following lists are valid input:
```
[1, 2, 3]
[1.0, "2", 3.1]
[1000]
```

**Outputs**

A normalized list of floats

**Example Usage**

```python
from RNAFoldAssess.utils.normalizers import *

some_list = [1.0, "2", 3.1]
normalized_list = Normalizers.simple_normalizer(some_list)
print(normalized_list)
# Will output: [0.3225806451612903, 0.6451612903225806, 1.0]
```

### 6.2.2 set_neg_to_0_and_normalize

Identical to `simple_normalizer` but sets all negative values in the given list to 0.

### 6.2.3 normalize_from_reactivity_map

Given a reactivity map, sets negative values to zero then normalizes reactivities then returns the reactivity map with updated normalized values. Note that a reactivity map is a data structure that maps chemical probing reactivity readings to their 0-indexed position in an RNA sequence. The dictionary keys are the RNA sequence positions and the values are reactivity readings.

**Inputs**

A reactivity map

**Outputs**

A reactivity map but with the normalized values

**Example Usage**

```python
from RNAFoldAssess.utils.normalizers import *

reactivity_map = {0: 0.3, 1: -2.5, 2: 5, 10: 2.3, 11: 4, 12: 1.2, 13: -4}
normalized_map = Normalizers.normalize_from_reactivity_map(reactivity_map)
print(normalized_map)
# Will output: {0: 0.06, 1: 0.0, 2: 1.0, 10: 0.45999999999999996, 11: 0.8, 12: 0.24, 13: 0.0}
```

### 6.2.4 align_sequence_with_reactivities

Given a sequence and reactivity map, this method returns a normalized reactivity map and fills in missing values. For example, if a sequence is 20 nucleotides long, but only positions 0 - 3 and 12 - 19 have reacitivty data, this method returns a reactivity map with the normalized data in positions 0 - 3 and 12 - 19, but also fills in a "0" for the positions 4 - 11.

**Inputs**

An RNA sequence and a reactivity map.

**Outputs**

A reactivity map with number of items equal to the number of nucleotides in the given RNA sequence

**Example Usage**

```python
from RNAFoldAssess.utils.normalizers import *

sequence = "AACCUUGGAACCUUGGGGAAUUCC"
reactivity_map = {0: 0.3, 1: -2.5, 2: 5, 10: 2.3, 11: 4, 12: 1.2, 13: -4}
aligned_map = Normalizers.align_sequence_with_reactivities(sequence, reactivity_map)
print(aligned_map)
# Will output: {0: 0.06, 1: 0.0, 2: 1.0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0.45999999999999996, 11: 0.8, 12: 0.24, 13: 0.0, 14: 0, 15: 0, 16: 0, 17: 0, 18: 0, 19: 0, 20: 0, 21: 0, 22: 0, 23: 0}
```

### 6.2.5 detect_reactivity_dropoff_in_polyA

This method helps detect the the poly(A) anomaly: progressive suppression of apparent reactivity across consecutive A’s in poly(A) stretches consistent with RTase bypass rather than true chemical protection. It returns a list of lists in which the inner lists are 0-indexed locations in the sequence in which the anomaly was detected.

**Inputs**

A sequence and reactivity_map are required. An option input `a_length` can be provided to indicate how many consectuive adenine's must have decreasing reactivity data for the data to be considered anomalous; the default value is 4.

**Outputs**

A list of lists in which each inner list is a range in the given sequence in which multiple adenine nucleotides show decreasing chemical mapping readings.

**Example Usage**

```python
seq = "CAAAACCAAAAAAU"
reactivity_map = {
    1: 0.1, 2: 0.2, 3: 0.4, 4: 0.45,
    5: 0.5, 6: 1, 7: 1, 8: 1, 9: 1
}
anomalous_spans = Normalizers.detect_reactivity_dropoff_in_polyA(seq, reactivity_map)
print(anomalous_spans)
# Will output: [[4, 3, 2, 1]]
```

## 6.3 PDBTools

The methods in `PDBTools` found in `utils/pdb_tools.py` provide some convenience functions for working with the protein databank.

### 6.3.1 get_pdb_file

This method takes a PDB ID and downloads its `.pdb` file from the protein databank.

**Inputs**

A protein databnk ID (e.g., 1EHZ). Users can optionally add a `destination_dir` to indicate where the pdb file should be downloaded; the default value is the current working directory.

**Outputs**

None

**Side Effects**

A PDB file is downloaded to the given destination directory.

**Example Usage**

```python
from RNAFoldAssess.utils.pdb_tools import *

PDBTools.get_pdb_file("1EHZ")
# The file 1EHZ.pdb is downloaded to the working directory.
```

### 6.3.2 get_mmcif_file

This method is identical to the `get_pdb_file` except that it downloads a `.cif` file instead of a `.pdb` file.

### 6.3.3 get_molecule_from_ebi

Returns molecule data from ChEMBL given a PDB Id.

**Inputs**

A PDB ID

**Outputs**

A list of dictionaries with molecule data from EBI.

**Example Usage**

```python
from RNAFoldAssess.utils.pdb_tools import *

molecule_data = PDBTools.get_molecule_from_ebi("1EHZ")
print(molecule_data)
# Will output:
# [{'molecule_type': 'polyribonucleotide', 'entity_id': 1, 'sample_preparation': 'Natural source', 'length': 76, 'number_of_copies': 1, 'in_chains': ['A'], 'in_struct_asyms': ['A'], 'mutation_flag': None, 'weight': 24890.121, 'ca_p_only': False, 'synonym': 'TRANSFER RNA (PHE)', 'molecule_name': ['TRANSFER RNA (PHE)'], 'gene_name': None, 'source': [{'organism_scientific_name': 'Saccharomyces cerevisiae', 'expression_host_scientific_name': None, 'tax_id': 4932, 'expression_host_tax_id': None, 'mappings': [{'start': {'residue_number': 1}, 'end': {'residue_number': 76}}]}], 'sequence': 'GCGGAUUUAGCUCAGUUGGGAGAGCGCCAGACUGAAGAUCUGGAGGUCCUGUGUUCGAUCCACAGAAUUCGCACCA', 'pdb_sequence': 'GCGGAUUUA(2MG)CUCAG(H2U)(H2U)GGGAGAGC(M2G)CCAGA(OMC)U(OMG)AA(YYG)A(PSU)(5MC)UGGAG(7MG)UC(5MC)UGUG(5MU)(PSU)CG(1MA)UCCACAGAAUUCGCACCA', 'pdb_sequence_indices_with_multiple_residues': ..., 'ca_p_only': False, 'molecule_name': ['water']}]
```

*Note that the above output data is truncated*

## 6.4 SecondaryStructureTools

The `SecondaryStructureTools` class found in `utils/secondary_structure_tools.py` provides several methods for working with and analyzing secondary structure data.

### 6.4.1 symmetric_chain

Given a dot-bracket string, return a boolean based on if the chain is symmetric (has as many open parentheses as closed ones). This may be useful when working with output from DSSR and structures are split between multiple chains.

**Inputs**

A dot-bracket notation string

**Outputs**

True/False value

**Example Usage**

```python
from RNAFoldAssess.utils.secondary_structure_tools import *

SecondaryStructureTools.symmetric_chain("((....))")
# True
SecondaryStructureTools.symmetric_chain("((....))...)")
# False
```

### 6.4.2 contains_pseudoknots

Given a dot-bracket notation string, returns True if pseudoknot syntax is found (square or curly brackets).

**Inputs**

A dot-bracket notation string

**Outputs**

True/False value

**Example Usage**

```python
from RNAFoldAssess.utils.secondary_structure_tools import *

SecondaryStructureTools.symmetric_chain("([....])")
# True
SecondaryStructureTools.symmetric_chain("((....))")
# False
```

### 6.4.3 parse_structure

This method returns the 0-indexed coordinates of all base pairs in a given dot-brakcet notation string. The coorinates are recorded in tuples where the first value is the 5' nucleotide position and the second value is the 3' nucleotide position. All coordinate tuples are returned in a list.

**Inputs**

A dot-bracket notation string

**Outputs**

A list of 2-tuples containing coordinates of basepairs.

**Example Usage**

```python
from RNAFoldAssess.utils.secondary_structure_tools import *

bn = "((...(....)..)..)..."
SecondaryStructureTools.parse_structure(dbn)
# [(0, 16), (1, 13), (5, 10)]
```

### 6.4.4 get_pairings

This method returns a list of basepaired nucleotides in a secondary structure. This can be helpful for detecting non-canonical base pairs in a given secondary structure. i.e., the secondary structure from sequence AAAA and dbn-string (..) indicates a base-pairing between two adenine nucleotides, which is not a Watson-Crick base pairing.

**Inputs**

An RNA sequence and dot-bracket notation string.

**Outputs**

A list of base-paired nucleotides.

**Example Usage**

```python
from RNAFoldAssess.utils.secondary_structure_tools import *

SecondaryStructureTools.get_pairings("CCAAAAGG", "((....))")
# ['CG', 'CG']
```

### 6.4.5 get_au_helix_end_pairs

Counts the number of consecutive AU pairs in the end of a given helix. This value is a parameter in the Turner 2004 model.

**Inputs**

A helix motif string. Note that a motif string follows the pattern of `{motif_type}_{sequence}_{dbn_string}`. For example: `HELIX_GUGGC&GUCAC_(((((&)))))`.

**Outputs**

Integer value of longest consecutive AU pairing at the end of the given helix (the "end" is defined as either the 5' or 3' side).

**Example Usage**

```python
from RNAFoldAssess.utils.secondary_structure_tools import *

motif = "HELIX_GAAAA&UUUUC_(((((&)))))"
SecondaryStructureTools.get_au_helix_end_pairs(motif)
# 4
```

### 6.4.6 helix_is_self_complementary_duplex

Takes a helix and returns a boolean value based on if the given helix is a self-complementary duplex. This value is a parameter in the Turner 2004 model.

**Inputs**

A helix motif string. Note that a motif string follows the pattern of `{motif_type}_{sequence}_{dbn_string}`. For example: `HELIX_GUGGC&GUCAC_(((((&)))))`.

**Outputs**

True/False value

**Example Usage**

```python
from RNAFoldAssess.utils.secondary_structure_tools import *

motif = "HELIX_GAAAA&UUUUC_(((((&)))))"
SecondaryStructureTools.helix_is_self_complementary_duplex(motif)
# True
motif = "HELIX_AGCU&AGUU_((((&))))" # Note the GU pair
SecondaryStructureTools.helix_is_self_complementary_duplex(motif)
# False
```

## 6.5 SequenceTools

The `SequenceTools` class found in `utils/sequence_tools.py` provides several methods for analyzing sequence data.

### 6.5.1 generate_kmers

Given a sequence and k value, returns a list of all k-mers in the given sequence.

**Inputs**

An RNA sequence and integer for k

**Outputs**

List of all k-mers from the given sequence.

**Example Usage**

```python
from RNAFoldAssess.utils.sequence_tools import *

SequenceTools.generate_kmers("AGCAGCAGCAGC", 3)
# ['AGC', 'GCA', 'CAG', 'AGC', 'GCA', 'CAG', 'AGC', 'GCA', 'CAG', 'AGC']
```

### 6.5.2 count_homopolymers

Given a sequence, condsecutive nucleotide length, and target nucleotide, returns the number of homopolymers of the given nucleotide in the given sequence.

**Inputs**

An RNA sequence, k. value (number of consecutive nucleotides to count as a hit), nucleotide.

**Outputs**

Number of target homopolymers in the given sequence.

**Example Usage**

```python
from RNAFoldAssess.utils.sequence_tools import *

SequenceTools.count_homopolymers("GAAGAAGAAA", 2, "A")
# 4
SequenceTools.count_homopolymers("GAAGAAGAAA", 3, "A")
# 1
```

### 6.5.3 get_gc_content

Returns the GC-content of a given sequence

**Inputs**

An RNA sequence

**Outputs**

A float value from 0 to 1

**Example Usage**

```python
from RNAFoldAssess.utils.sequence_tools import *

SequenceTools.get_gc_content("CCCCAAAAUUUUGGGG")
# 0.5
```

### 6.5.4 get_sequence_entropy

Returns the Shannon Entropy value of a sequence (using log base 4). This value may be useful for some analysis tasks and is used in the original study for which this framework was developed. As such, it is provided for convenience.

**Inputs**

An RNA sequence and optionally a log base. The default value for the log base is 4 since there are 4 nucelotides, but users may find value in using different bases.

**Outputs**

A float value of the sequence's Shannon Entropy

**Example Usage**

```python
from RNAFoldAssess.utils.sequence_tools import *

SequenceTools.get_sequence_entropy("AAAAAAAA")
# 0.0
SequenceTools.get_sequence_entropy("AAAAGGGG")
# 0.5
SequenceTools.get_sequence_entropy("ACGUACGU")
# 1.0
```

# 7 Contact

For any questions, please contact Erik Whiting at `ewhiting4@huskers.unl.edu`

<!--
Will find a better section for this later

## Usage

The RNAFoldAssess framework essentially supports the construction of pipelines for comparing the performance of multiple secondary structure prediction tools against large collections of data. There are several utility functions and extendable classes available to users, but the main power is in the `PredictionPipeline` class. This class provides static methods for running pipelines by taking in RNA data in a standardized format and a Python object wrapping a prediction tool. Consider the following example:

```python
# This is not runnable code, it is just an example

from RNAFoldAssess.models import DataPoint, PredictionPipeline
from RNAFoldAssess.models.predictors import RNAFold, RNAStructure, IPKnot


# initialize predictor models
models = [RNAFold(), RNAStructure(), IPKnot()]

datapoints = DataPoint.init_from_csv_file("path/to/rna_data.csv")

for m in models:
    PredictionPipeline.run_prediction(
        datapoints,
        m,
        output_path=f"path/to/analysis_path/{m}_predictions_and_evaluations.csv"
    )
```

The above code initializes three `predictor` objects, one wrapping RNAFold, one wrapping RNAStructure, and one wrapping IPKnot, and puts them in a Python list. Then, the code imports RNA data via the `DataPoint.init_from_csv_file` method. Then, the code loops through the list of models and kicks off a pipeline for each. The pipeline is using the given model to predict the secondary structure of each RNA in the `datapoints` list, evaluating the accuracy of that prediction, and then writing the predictions and evaluations to the file specified in `output_path`.

When the above example has cmopleted, the user will have 3 CSV files--one for each model--each containing the RNA name, sequence, secondary structure prediction, and evaluation. The user can then do additional analysis between the 3 files to evaluate which models are better at what. -->



<!-- ### Adding a Custom Scorer

Need to find a home for this

Some researchers may want to customize the scoring method while still using the RNAFoldAssess framework. To do so, add a `.py` file to the `models/scorers` directory and create a class that inherits `Scorer`. The `Scorer` class is a base class that defines the two methods a scorer class needs to plug into the framework: `evaluate` and `report`. The `scorer.py` class has more detailed instructions for implementing a new scorer. Scoring methods should base their calculations on a prediction in dbn format, as these are what the `Predictor` models output. -->
